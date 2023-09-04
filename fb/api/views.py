from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connections, DatabaseError, IntegrityError
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.db.utils import DataError

def set_card_description_internal(description = ""):
    with connections['default'].cursor() as cursor:
        description_id_obj = cursor.var(int)
        sql_query = "INSERT INTO CARD_DESCRIPTION (init_time, update_time, description) VALUES (SYSDATE, SYSDATE, %s) RETURNING description_id INTO %s"
        cursor.execute(sql_query, [description, description_id_obj])
        description_id = description_id_obj.getvalue()[0]
    return description_id

def set_media_internal(uploaded_image, type = 'image'):
    fs = FileSystemStorage(location='G:/Website_Project/From_Git/fbproject/frontend/public/images/storage')
    with connections['default'].cursor() as cursor:
        media_id_obj = cursor.var(int)
        sql_query = "INSERT INTO MEDIA (media_type) VALUES (%s) RETURNING media_id INTO %s"
        cursor.execute(sql_query, [type, media_id_obj])
        media_id = media_id_obj.getvalue()[0]
    image_name = str(media_id)
    fs.save(image_name, uploaded_image)
    print('world')
    return media_id

def set_card_description_media_internal(description_id, media_id):
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO CARD_DESCRIPTION_MEDIA (description_id, media_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [description_id, media_id])

def set_post_internal(user_id, description_id, type = 'user_post'):
    with connections['default'].cursor() as cursor:
        post_id_obj = cursor.var(int)
        sql_query = "INSERT INTO POST (user_id, description_id, post_of) VALUES (%s, %s, %s) RETURNING post_id INTO %s"
        print('start')
        cursor.execute(sql_query, [user_id, description_id, type, post_id_obj])
        print('end')
        post_id = post_id_obj.getvalue()[0]
    return post_id

def set_card_description_with_media_internal(description, uploaded_images):
    description_id = set_card_description_internal(description)
    for uploaded_image in uploaded_images:
        media_id = set_media_internal(uploaded_image)
        print('hello')
        set_card_description_media_internal(description_id, media_id)
    return description_id

def set_user_internal(user_name, password, mobile_number, birth_date, email):
    with connections['default'].cursor() as cursor:
        user_id_obj = cursor.var(int)
        sql_query = "INSERT INTO USERS (user_name, password, mobile_number, birth_date, email) VALUES (%s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'), %s) RETURNING user_id INTO %s"
        cursor.execute(sql_query, [user_name, password, mobile_number, birth_date, email, user_id_obj])
        user_id = user_id_obj.getvalue()[0]
    return user_id

def set_profile_pic_internal(uploaded_image, user_id):
    media_id = set_media_internal(uploaded_image)
    description_id = set_card_description_internal()
    set_card_description_media_internal(description_id, media_id)
    with connections['default'].cursor() as cursor:
        post_id_obj = cursor.var(int)
        sql_query = "INSERT INTO POST (user_id, description_id, post_of) VALUES (%s, %s, 'profilepic') RETURNING post_id INTO %s"
        cursor.execute(sql_query, [user_id, description_id, post_id_obj])
        post_id = post_id_obj.getvalue()[0]
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO USER_PROFILE_PIC (user_id, post_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [user_id, post_id])
    return JsonResponse({'message': 'Image uploaded successfully'})

def set_cover_photo_internal(uploaded_image, user_id):
    media_id = set_media_internal(uploaded_image)
    description_id = set_card_description_internal()
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO CARD_DESCRIPTION_MEDIA (description_id, media_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [description_id, media_id])
    with connections['default'].cursor() as cursor:
        post_id_obj = cursor.var(int)
        sql_query = "INSERT INTO POST (user_id, description_id, post_of) VALUES (%s, %s, 'coverphoto') RETURNING post_id INTO %s"
        cursor.execute(sql_query, [user_id, description_id, post_id_obj])
        post_id = post_id_obj.getvalue()[0]
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO USER_COVER_PHOTO (user_id, post_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [user_id, post_id])
    return JsonResponse({'message': 'Image uploaded successfully'})

def get_post_info_internal(post_id):
    try:
        post_data = {}
        
        # card_description
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT P.user_id, CD.init_time, CD.update_time, CD.description FROM POST P "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
            sql_query += "WHERE P.post_id = %s"
            cursor.execute(sql_query, [post_id])
            row = cursor.fetchall()[0]
            user_id = row[0]
            init_time = row[1]
            update_time = row[2]
            description = row[3]
            post_data['user_id'] = user_id
            post_data['init_time'] = init_time
            post_data['update_time'] = update_time
            post_data['description'] = description
        
        # user
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT U.user_name, CDM.media_id FROM POST P "
            sql_query += "JOIN USERS U ON P.user_id = U.user_id "
            sql_query += "JOIN USER_PROFILE_PIC UPP ON U.user_id = UPP.user_id "
            sql_query += "JOIN POST P2 ON UPP.post_id = P2.post_id "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P2.description_id = CD.description_id "
            sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
            sql_query += "WHERE P.post_id = %s "
            sql_query += "ORDER BY CDM.media_id DESC"
            cursor.execute(sql_query, [post_id])
            row = cursor.fetchall()[0]
            user_name = row[0]
            profile_pic = row[1]
            post_data['user_name'] = user_name
            post_data['profile_pic'] = profile_pic
        
        # media
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT CDM.media_id FROM POST P "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
            sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
            sql_query += "WHERE P.post_id = %s "
            sql_query += "ORDER BY CDM.media_id"
            cursor.execute(sql_query, [post_id])
            rows = cursor.fetchall()
            media = []
            for row in rows:
                media.append('/images/storage/'+str(row[0]))
            post_data['media'] = media
        
        # reaction count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM POST_REACT "
            sql_query += "WHERE post_id = %s "
            cursor.execute(sql_query, [post_id])
            react_count = cursor.fetchall()[0]
            post_data['react_count'] = react_count[0]
        
        # share count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM POST_SHARED_BY_USER "
            sql_query += "WHERE post_id = %s AND user_id = %s"
            cursor.execute(sql_query, [post_id, user_id])
            share_count = cursor.fetchall()[0]
            post_data['share_count'] = share_count[0]
        
        # comment count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM POST_COMMENT "
            sql_query += "WHERE post_id = %s"
            cursor.execute(sql_query, [post_id])
            comment_count = cursor.fetchall()[0]
            post_data['comment_count'] = comment_count[0]
        
        return post_data
    except Exception as e:
        print(f"An exception occurred: {e}")
        return  ({'message':'error'})

def get_user_post_id_internal(user_id):
    try:
        with connections['default'].cursor() as cursor:
            sql_query  = "SELECT P.post_id FROM POST P "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
            sql_query += "WHERE P.user_id =%s "
            sql_query += "ORDER BY CD.update_time"
            cursor.execute(sql_query, [user_id])
            rows = cursor.fetchall()
        all_post_id =[]
        for row in rows:
            all_post_id.append(row[0])
        return all_post_id
    except Exception as e:
        print(f"An exception occurred: {e}")
        return ({'message':'error'})

@api_view(['POST'])
def homePage(request):
    user_id = request.data.get('user_id')
    post_ids = get_user_post_id_internal(user_id)
    post_infos = []
    for post_id in post_ids:
        post_info = get_post_info_internal(post_id)
        post_infos.append(post_info)
    return Response(post_infos)

@api_view(['POST'])
def signIn(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return JsonResponse({'error': 'Both email and password are required.'}, status=400)
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT user_id FROM USERS WHERE email = %s AND password = %s"
            cursor.execute(sql_query, [email, password])
            rows = cursor.fetchall()
        if not rows:
            return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        user_id = rows[0][0]
        return Response({'user_id': user_id})
    except DatabaseError as e:
        return JsonResponse({'error': 'Database error occurred.'}, status=500)
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)

@api_view(['POST'])
def setUsers(request):
    try:
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        mobile_number = request.POST.get('mobile')
        birth_date = request.POST.get('birth_date')
        email = request.POST.get('email')
        profile_pic = request.FILES['profile_pic']
        cover_photo = request.FILES['cover_photo']
        print(user_name, password, mobile_number, birth_date, email)
        if user_name and password and mobile_number and birth_date and email:
            user_id = set_user_internal(user_name, password, mobile_number, birth_date, email)
            if profile_pic:
                set_profile_pic_internal(profile_pic, user_id)
            if cover_photo:
                set_cover_photo_internal(cover_photo, user_id)
        return JsonResponse({"message": "User created successfully"})
    except IntegrityError:
        return Response({"error": "IntegrityError: User already exists"}, status=400)
    except DataError:
        return Response({"error": "DataError: Invalid data format"}, status=400)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)

@api_view(['POST'])
def set_user_post(request):
    try:
        user_id = request.POST.get('user_id')
        description = request.POST.get('description')
        uploaded_image = request.FILES['media']
        print(1)
        media_id = set_media_internal(uploaded_image)
        description_id = set_card_description_internal(description)
        set_card_description_media_internal(description_id, media_id)
        print(2)
        post_id = set_post_internal(user_id, description_id, 'user_post')
        print(3)
        return JsonResponse({'message': 'Image uploaded successfully'})
    except IntegrityError:
        return Response({"error": "IntegrityError: User already exists"}, status=400)
    except DataError:
        return Response({"error": "DataError: Invalid data format"}, status=400)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)

@api_view(['POST'])
def get_groups(request):
    user_id = request.data.get('user_id')
    group_type = request.data.get('group_type')
    groups_data = []
    with connections['default'].cursor() as cursor:
        sql_query  = 'SELECT G.group_id, G.group_name, G.description_id, CD.description, CD.init_time,  CD.update_time FROM GROUPS G '
        sql_query += 'JOIN CARD_DESCRIPTION CD ON G.description_id = CD.description_id '
        sql_query += 'JOIN GROUP_MEMBERS GM ON GM.group_id = G.group_id '
        sql_query += 'WHERE GM.user_id = %s AND G.group_type = %s '
        sql_query += 'GROUP BY G.group_id, G.group_name, G.description_id, CD.description, CD.init_time,  CD.update_time '
        cursor.execute(sql_query, [user_id, group_type])
        rows = cursor.fetchall()
    for row in rows:
        group_id = row[0]
        group_name = row[1]
        description_id = row[2]
        description = row[3]
        init_time = row[4]
        update_time = row[5]
        with connections['default'].cursor() as cursor:
            sql_query  = 'SELECT CDM.media_id FROM CARD_DESCRIPTION_MEDIA CDM '
            sql_query += 'JOIN CARD_DESCRIPTION CD ON CDM.description_id = CD.description_id '
            sql_query += 'WHERE CD.description_id = %s '
            sql_query += 'ORDER BY CD.init_time '
            cursor.execute(sql_query, [description_id])
            rows2 = cursor.fetchall()
            media = []
            for row2 in rows2:
                
                media.append('/images/storage/'+str(row2[0]))
                
            group_data = {}
            group_data['group_id'] = group_id
            group_data['group_name'] = group_name
            group_data['media'] = media
            group_data['description'] = description
            group_data['init_time'] = init_time
            group_data['update_time'] = update_time
            groups_data.append(group_data)
    return Response(groups_data)

@api_view(['POST'])
def get_friend_list(request):
    try:
        user_id = request.data.get('user_id')
        profile_data = []

        # friend_data
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT U.user_id, U.user_name FROM BEFRIENDS B "
            sql_query += "JOIN USERS U ON B.friend_id = U.user_id "
            sql_query += "WHERE B.user_id = %s "
            sql_query += "UNION "
            sql_query +=  "SELECT U.user_id, U.user_name FROM BEFRIENDS B "
            sql_query += "JOIN USERS U ON B.user_id = U.user_id "
            sql_query += "WHERE B.friend_id = %s "
            cursor.execute(sql_query, [user_id, user_id])
            rows = cursor.fetchall()
        for row in rows:
            friend_id = row[0]
            user_name = row[1]
            with connections['default'].cursor() as cursor:
                sql_query  = "SELECT CDM.media_id FROM USER_PROFILE_PIC UPP "
                sql_query += "JOIN POST P ON UPP.post_id = P.post_id "
                sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
                sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
                sql_query += "WHERE UPP.user_id = %s "
                sql_query += "ORDER BY CD.update_time"
                cursor.execute(sql_query, [friend_id])
                rows2 = cursor.fetchall()
                media = []
                for row2 in rows2:
                    media.append('/images/storage/'+str(row2[0]))
                # print(media)
                temp_obj = {}
                temp_obj['user_id'] = user_id
                temp_obj['user_name'] = user_name
                temp_obj['media'] = media
                profile_data.append(temp_obj)
        #         print(temp_obj)
        # print(profile_data)
        return Response(profile_data)
    except Exception as e:
        return JsonResponse({'message': 'error'})

@api_view(['POST'])
def get_friend_req_list(request):
    try:
        user_id = request.data.get('user_id')
        profile_data = []

        # friend_data
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT U.user_id, U.user_name FROM FRIEND_REQ FR "
            sql_query += "JOIN USERS U ON FR.friend_req_id = U.user_id "
            sql_query += "WHERE FR.user_id = %s "
            cursor.execute(sql_query, [user_id])
            rows = cursor.fetchall()
            print(rows)
        for row in rows:
            friend_id = row[0]
            user_name = row[1]
            with connections['default'].cursor() as cursor:
                sql_query  = "SELECT CDM.media_id FROM USER_PROFILE_PIC UPP "
                sql_query += "JOIN POST P ON UPP.post_id = P.post_id "
                sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
                sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
                sql_query += "WHERE UPP.user_id = %s "
                sql_query += "ORDER BY CD.update_time"
                cursor.execute(sql_query, [friend_id])
                rows2 = cursor.fetchall()
                media = []
                for row2 in rows2:
                    media.append('/images/storage/'+str(row2[0]))
                # print(media)
                temp_obj = {}
                temp_obj['user_id'] = user_id
                temp_obj['user_name'] = user_name
                temp_obj['media'] = media
                profile_data.append(temp_obj)
        #         print(temp_obj)
        # print(profile_data)
        return Response(profile_data)
    except Exception as e:
        return JsonResponse({'message': 'error'})

@api_view(['POST'])
def set_group(request):
    user_id = request.POST.get('user_id')
    group_name = request.POST.get('group_name')
    description = request.POST.get('description')
    print('hello')
    uploaded_image = request.FILES['media']
    group_type = request.POST.get('group_type')
    media_id = set_media_internal(uploaded_image)
    description_id = set_card_description_internal(description)
    set_card_description_media_internal(description_id, media_id)

    with connections['default'].cursor() as cursor:
        group_id_obj = cursor.var(int)
        sql_query = "INSERT INTO GROUPS (group_name, description_id, group_type) VALUES (%s, %s, %s) RETURNING group_id INTO %s"
        cursor.execute(sql_query, [group_name, description_id, group_type, group_id_obj])
        group_id = group_id_obj.getvalue()[0]

    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO GROUP_MEMBERS (user_id, group_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [user_id, group_id])
    
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO GROUP_OWNED (user_id, group_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [user_id, group_id])
    
    return JsonResponse({'message': 'Image uploaded successfully'})

@api_view(['POST'])
def get_chat_friend_list(request):
    try:
        user_id = request.data.get('user_id')
        profile_data = []

        # friend_data
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT U.user_id, U.user_name FROM BEFRIENDS B "
            sql_query += "JOIN USERS U ON B.user_id = U.user_id "
            sql_query += "WHERE B.friend_id = %s "
            sql_query += "AND EXISTS( "
            sql_query += "SELECT * FROM MESSAGE M "
            sql_query += "WHERE (M.sender_id = B.user_id AND M.receiver_id = B.friend_id) "
            sql_query += "OR (M.receiver_id = B.user_id AND M.sender_id = B.friend_id) "
            sql_query += ") "
            sql_query += "UNION "
            sql_query += "SELECT U.user_id, U.user_name FROM BEFRIENDS B "
            sql_query += "JOIN USERS U ON B.friend_id = U.user_id "
            sql_query += "WHERE B.user_id = %s "
            sql_query += "AND EXISTS( "
            sql_query += "SELECT * FROM MESSAGE M "
            sql_query += "WHERE (M.sender_id = B.user_id AND M.receiver_id = B.friend_id) "
            sql_query += "OR (M.receiver_id = B.user_id AND M.sender_id = B.friend_id) "
            sql_query += ") "
            cursor.execute(sql_query, [user_id, user_id])
            rows = cursor.fetchall()
        print(2)
        for row in rows:
            friend_id = row[0]
            user_name = row[1]
            with connections['default'].cursor() as cursor:
                sql_query = "SELECT CD.description, CD.init_time FROM MESSAGE M "
                sql_query += "JOIN CARD_DESCRIPTION CD ON CD.description_id = M.description_id "
                sql_query += "WHERE M.sender_id = %s AND M.receiver_id = %s "
                sql_query += "OR M.sender_id = %s AND M.receiver_id = %s "
                sql_query += "ORDER BY CD.init_time DESC "
                cursor.execute(sql_query, [user_id, friend_id, friend_id, user_id])
                messages = cursor.fetchall()
                last_message =  messages[0][0]
                last_message_time = messages[0][1]
            print(3)
            with connections['default'].cursor() as cursor:
                sql_query  = "SELECT CDM.media_id FROM USER_PROFILE_PIC UPP "
                sql_query += "JOIN POST P ON UPP.post_id = P.post_id "
                sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
                sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
                sql_query += "WHERE UPP.user_id = %s "
                sql_query += "ORDER BY CD.update_time"
                cursor.execute(sql_query, [friend_id])
                rows2 = cursor.fetchall()
                media = []
                for row2 in rows2:
                    media.append('/images/storage/'+str(row2[0]))
                # print(media)
                temp_obj = {}
                temp_obj['user_id'] = user_id
                temp_obj['user_name'] = user_name
                temp_obj['media'] = media
                temp_obj['last_message'] = last_message
                temp_obj['last_message_time'] = last_message_time
                profile_data.append(temp_obj)
            print(4)
        #         print(temp_obj)
        # print(profile_data)
        return Response(profile_data)
    except Exception as e:
        return JsonResponse({'message': 'error'})

@api_view(['POST'])
def get_events(request):
    print(0)
    user_id = request.data.get('user_id')
    group_type = 'event'
    groups_data = []
    with connections['default'].cursor() as cursor:
        sql_query  = 'SELECT E.event_id, E.start_time, E.end_time, E.location, G.group_id, G.group_name, G.description_id, CD.description, CD.init_time, CD.update_time FROM EVENTS E '
        sql_query += 'JOIN GROUPS G ON E.group_id = G.group_id '
        sql_query += 'JOIN CARD_DESCRIPTION CD ON G.description_id = CD.description_id '
        sql_query += 'JOIN GROUP_MEMBERS GM ON GM.group_id = G.group_id '
        sql_query += 'WHERE GM.user_id = %s AND G.group_type = %s '
        sql_query += 'GROUP BY E.event_id, E.start_time, E.end_time, E.location, G.group_id, G.group_name, G.description_id, CD.description, CD.init_time, CD.update_time '
        print(1)
        cursor.execute(sql_query, [user_id, group_type])
        print(2)
        rows = cursor.fetchall()
    for row in rows:
        event_id = row[0]
        start_time = row[1]
        end_time = row[2]
        location = row[3]
        group_id = row[4]
        group_name = row[5]
        description_id = row[6]
        description = row[7]
        init_time = row[8]
        update_time = row[9]
        with connections['default'].cursor() as cursor:
            sql_query  = 'SELECT CDM.media_id FROM CARD_DESCRIPTION_MEDIA CDM '
            sql_query += 'JOIN CARD_DESCRIPTION CD ON CDM.description_id = CD.description_id '
            sql_query += 'WHERE CD.description_id = %s '
            sql_query += 'ORDER BY CD.init_time '
            cursor.execute(sql_query, [description_id])
            rows2 = cursor.fetchall()
            media = []
            for row2 in rows2:
                
                media.append('/images/storage/'+str(row2[0]))
                
            group_data = {}
            group_data['event_id'] = event_id
            group_data['start_time'] = start_time
            group_data['end_time'] = end_time
            group_data['location'] = location
            group_data['event_name'] = group_name
            group_data['media'] = media
            group_data['description'] = description
            group_data['init_time'] = init_time
            group_data['update_time'] = update_time
            groups_data.append(group_data)
    return Response(groups_data)

@api_view(['POST'])
def set_event(request):
    user_id = request.POST.get('user_id')
    event_name = request.POST.get('event_name')
    description = request.POST.get('description')
    uploaded_image = request.FILES['media']
    group_type = 'event'
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    location = request.POST.get('location')
    media_id = set_media_internal(uploaded_image)
    description_id = set_card_description_internal(description)
    set_card_description_media_internal(description_id, media_id)

    with connections['default'].cursor() as cursor:
        group_id_obj = cursor.var(int)
        sql_query = "INSERT INTO GROUPS (group_name, description_id, group_type) VALUES (%s, %s, %s) RETURNING group_id INTO %s"
        cursor.execute(sql_query, [event_name, description_id, group_type, group_id_obj])
        group_id = group_id_obj.getvalue()[0]

    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO GROUP_MEMBERS (user_id, group_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [user_id, group_id])
    
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO GROUP_OWNED (user_id, group_id) VALUES (%s, %s)"
        cursor.execute(sql_query, [user_id, group_id])
    
    with connections['default'].cursor() as cursor:
        sql_query = "INSERT INTO EVENTS (start_time, end_time, location, group_id) VALUES (TO_DATE(%s, 'YYYY-MM-DD'), TO_DATE(%s, 'YYYY-MM-DD'), %s, %s)"
        cursor.execute(sql_query, [start_time, end_time, location,  group_id])
    
    return JsonResponse({'message': 'Image uploaded successfully'})

@api_view(['POST'])
def search_users(request):
    query = request.data.get('key')
    sql_query = 'SELECT user_id, user_name FROM users WHERE LOWER(user_name) LIKE %s'
    with connections['default'].cursor() as cursor:
        cursor.execute(sql_query, ['%' + str(query).lower() + '%'])
        print('%' + str(query).lower() + '%')
        results = cursor.fetchall()
        serialized_results = [{"id": user_id, "user_name": user_name} for user_id, user_name in results]
        print(serialized_results)
    # serialized_results.append({"error":"hello"})
    return Response(serialized_results)

@api_view(['POST'])
def get_marketplace(request):
    with connections['default'].cursor() as cursor:
        sql_query  = "SELECT M.product_name, M.price, CD.description, CD.init_time, CD.update_time, P.user_id, CD.description_id, U.user_id FROM MARKETPLACE M "
        sql_query += "JOIN POST P ON M.POST_ID = P.POST_ID "
        sql_query += "JOIN CARD_DESCRIPTION CD ON P.DESCRIPTION_ID = CD.DESCRIPTION_ID "
        sql_query += "JOIN USERS U ON U.USER_ID = P.USER_ID "
        cursor.execute(sql_query)
        rows = cursor.fetchall()
    posts = []
    for row in rows:
        product_name = row[0]
        price = row[1]
        description = row[2]
        init_time = row[3]
        update_time = row[4]
        user_id = row[5]
        description_id = row[6]
        user_name = row[7]

        with connections['default'].cursor() as cursor:
            sql_query = "SELECT CDM.media_id FROM USER_PROFILE_PIC UPP "
            sql_query += "JOIN POST P ON P.POST_ID=UPP.POST_ID  "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P.DESCRIPTION_ID=CD.DESCRIPTION_ID  "
            sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.DESCRIPTION_ID=CDM.DESCRIPTION_ID  "
            sql_query += "WHERE UPP.user_id = %s "
            cursor.execute(sql_query, [user_id])
            rows2 = cursor.fetchall()
            profile_pic = []
            for row2 in rows2:
                profile_pic.append('/images/storage/'+str(row2[0]))

        with connections['default'].cursor() as cursor:
            sql_query  = 'SELECT CDM.media_id FROM CARD_DESCRIPTION_MEDIA CDM '
            sql_query += 'JOIN CARD_DESCRIPTION CD ON CDM.description_id = CD.description_id '
            sql_query += 'WHERE CD.description_id = %s '
            sql_query += 'ORDER BY CD.init_time '
            cursor.execute(sql_query, [description_id])
            rows2 = cursor.fetchall()
            media = []
            for row2 in rows2:
                media.append('/images/storage/'+str(row2[0]))
        
        temp_obj = {}
        temp_obj['product_name'] = product_name
        temp_obj['price'] = price
        temp_obj['description'] = description
        temp_obj['init_time'] = init_time
        temp_obj['update_time'] = update_time
        temp_obj['user_id'] = user_id
        temp_obj['user_name'] = user_name
        temp_obj['profile_pic'] = profile_pic
        temp_obj['media'] = media
        posts.append(temp_obj)
        
    print(posts)

    return Response(posts)


@api_view(['POST'])
def set_marketplace(request):
    user_id = request.POST.get('user_id')
    product_name = request.POST.get('product_name')
    price = request.POST.get('price')
    description = request.POST.get('description')
    print('hello')
    uploaded_image = request.FILES['media']
    post_type = 'market'
    media_id = set_media_internal(uploaded_image)
    description_id = set_card_description_internal(description)
    set_card_description_media_internal(description_id, media_id)
    post_id = set_post_internal(user_id, description_id, post_type)
    print('pid: ', post_id)
    print(product_name, price)
    with connections['default'].cursor() as cursor:
        marketplace_id_obj = cursor.var(int)
        sql_query = "INSERT INTO MARKETPLACE (PRODUCT_NAME, PRICE, POST_ID ) VALUES (%s, %s, %s) RETURNING marketplace_id INTO %s"
        cursor.execute(sql_query, [product_name, price, post_id, marketplace_id_obj])
        marketplace_id = marketplace_id_obj.getvalue()[0]
    
    return JsonResponse({'message': 'Image uploaded successfully'})


# @api_view(['POST'])
# def get_user_profile(request):
#     try:
#         user_id = request.POST.get('user_id')
#         profile_data = {}

#         # profile_pic
#         with connections['default'].cursor() as cursor:
#             sql_query =  "SELECT CDM.media_id FROM USERS U "
#             sql_query += "JOIN USER_PROFILE_PIC UPP ON U.user_id = UPP.user_id "
#             sql_query += "JOIN POST P ON UPP.post_id = P.post_id "
#             sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
#             sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.media_id = CDM.media_id "
#             sql_query += "WHERE user_id = %s "
#             sql_query += "ORDER BY CDM.media_id DESC"
#             cursor.execute(sql_query, [user_id])
#             profile_pic = cursor.fetchall()[0]
#             profile_data['profile_pic'] = profile_pic
        
#         # cover_photo
#         with connections['default'].cursor() as cursor:
#             sql_query =  "SELECT CDM.media_id FROM USERS U "
#             sql_query += "JOIN USER_COVER_PHOTO UCP ON U.user_id = UCP.user_id "
#             sql_query += "JOIN POST P ON UCP.post_id = P.post_id "
#             sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
#             sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.media_id = CDM.media_id "
#             sql_query += "WHERE user_id = %s "
#             sql_query += "ORDER BY CDM.media_id DESC"
#             cursor.execute(sql_query, [user_id])
#             cover_photo = cursor.fetchall()[0]
#             profile_data['cover_photo'] = cover_photo
        
#         # user_data
#         with connections['default'].cursor() as cursor:
#             sql_query =  "SELECT user_name FROM USERS "
#             sql_query += "WHERE user_id = %s"
#             cursor.execute(sql_query, [user_id])
#             user_name = cursor.fetchall()[0]
#             profile_data['user_name'] = user_name
        
#         # friends count
#         with connections['default'].cursor() as cursor:
#             sql_query =  "SELECT COUNT(*) FROM BEFRIENDS "
#             sql_query += "WHERE user_id = %s "
#             sql_query += "OR friend_id = %s"
#             cursor.execute(sql_query, [user_id])
#             friend_count = cursor.fetchall()[0]
#             profile_data['friend_count'] = friend_count[0]
        
#         return Response(profile_data)
#     except Exception as e:
#         return JsonResponse({'message': 'error'})




