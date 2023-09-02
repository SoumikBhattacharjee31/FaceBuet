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
        sql_query = "INSERT INTO POST (user_id, description_id, post_of) VALUES (%s, %s, %s) RETURNING description_id INTO %s"
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






