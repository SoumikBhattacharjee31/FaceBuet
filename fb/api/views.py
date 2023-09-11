from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connections, DatabaseError, IntegrityError
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.db.utils import DataError
import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
# from .utils import delete_file
image_path = '/images/storage/'
absolute_image_path = 'G:/Website_Project/From_Git/fbproject/frontend/public/images/storage'

def delete_file(file_path):
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error deleting file: {str(e)}")
        return False



def set_card_description_internal(description = ""):
    try:
        if not description:
            description=""
        with connections['default'].cursor() as cursor:
            description_id_obj = cursor.var(int)
            sql_query = "INSERT INTO CARD_DESCRIPTION (init_time, update_time, description) VALUES (SYSDATE, SYSDATE, %s) RETURNING description_id INTO %s"
            cursor.execute(sql_query, [description, description_id_obj])
            description_id = description_id_obj.getvalue()[0]
        return description_id
    except Exception as e:
        print("Error Setting Card Description: "+str(e))

def set_media_internal(uploaded_image, type = 'image'):
    try:
        if not  uploaded_image or not type:
            print("Invalid Input")
            return
        with connections['default'].cursor() as cursor:
            media_id_obj = cursor.var(int)
            sql_query = "INSERT INTO MEDIA (media_type) VALUES (%s) RETURNING media_id INTO %s"
            cursor.execute(sql_query, [type, media_id_obj])
            media_id = media_id_obj.getvalue()[0]
        image_name = str(media_id)
        fs = FileSystemStorage(location=absolute_image_path)
        fs.save(image_name, uploaded_image)
        return media_id
    except Exception as e:
        print("Error Setting Media: "+str(e))

def set_card_description_media_internal(description_id, media_id):
    try:
        if not description_id or not media_id:
            print("Invalid Input")
            return
        with connections['default'].cursor() as cursor:
            sql_query = "INSERT INTO CARD_DESCRIPTION_MEDIA (description_id, media_id) VALUES (%s, %s)"
            cursor.execute(sql_query, [description_id, media_id])
    except Exception as e:
        print("Error Setting Card Description Media: "+str(e))

def set_post_internal(user_id, description_id, type = 'user_post'):
    try:
        if not user_id or not description_id or not type:
            print("Invalid Input")
            return
        with connections['default'].cursor() as cursor:
            post_id_obj = cursor.var(int)
            sql_query = "INSERT INTO POST (user_id, description_id, post_of) VALUES (%s, %s, %s) RETURNING post_id INTO %s"
            cursor.execute(sql_query, [user_id, description_id, type, post_id_obj])
            post_id = post_id_obj.getvalue()[0]
        return post_id
    except Exception as e:
        print("Error Setting Post: "+str(e))

def set_card_description_with_multiple_media_internal(uploaded_images,description=""):
    try:
        description_id = set_card_description_internal(description)
        if uploaded_image:
            for uploaded_image in uploaded_images:
                media_id = set_media_internal(uploaded_image)
                set_card_description_media_internal(description_id, media_id)
            return description_id
    except Exception as e:
        print("Error Setting Card Description With Media: "+str(e))

def set_user_internal(user_name, password, mobile_number, birth_date, email):
    try:
        if not user_name or not password or not mobile_number or not birth_date or not email:
            print("Invalid Input")
            return
        with connections['default'].cursor() as cursor:
            user_id_obj = cursor.var(int)
            sql_query = "INSERT INTO USERS (user_name, password, mobile_number, birth_date, email) VALUES (%s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'), %s) RETURNING user_id INTO %s"
            cursor.execute(sql_query, [user_name, password, mobile_number, birth_date, email, user_id_obj])
            user_id = user_id_obj.getvalue()[0]
        return user_id
    except Exception as e:
        print("Error Setting User: "+str(e))
        return False

def set_profile_pic_internal(uploaded_image, user_id):
    try:
        if not uploaded_image or not user_id:
            print("Invalid Input")
            return
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
    except Exception as e:
        print("Error Setting Profile Pic: "+str(e))

def set_cover_photo_internal(uploaded_image, user_id):
    try:
        if not uploaded_image or not user_id:
            print("Invalid Input")
            return
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
    except Exception as e:
        print("Error Setting Cover Photo: "+str(e))
        return ("error")

def get_user_name_and_single_profile_pic_from_user_id_internal(user_id):
    try:
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT user_name FROM USERS "
            sql_query+= "WHERE user_id = %s "
            cursor.execute(sql_query,[user_id])
            user_name = cursor.fetchall()[0][0]
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT create_media_url(CDM.media_id) FROM USER_PROFILE_PIC UPP "
            sql_query+= "JOIN POST P ON UPP.post_id = P.post_id "
            sql_query+= "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
            sql_query+= "JOIN CARD_DESCRIPTION_MEDIA CDM ON P.description_id = CDM.description_id "
            sql_query+= "WHERE UPP.user_id = %s "
            sql_query+= "ORDER BY CD.init_time DESC "
            cursor.execute(sql_query,[user_id])
            medias = cursor.fetchall()
            try:
                media = medias[0][0]
            except Exception as e:
                media = ""
        data = {}
        data['user_id'] = user_id
        data['user_name'] = user_name
        data['profile_pic'] = media
        return data
    except Exception as e:
        print ("Error Getting User Name And Profile Pic From User ID: "+str(e))
def get_group_name_and_single_media_from_group_id_internal(group_id):
    try:
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT group_name FROM GROUPS "
            sql_query+= "WHERE group_id = %s "
            cursor.execute(sql_query,[group_id])
            user_name = cursor.fetchall()[0][0]
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT create_media_url(CDM.media_id) FROM GROUPS G "
            sql_query+= "JOIN CARD_DESCRIPTION CD ON G.description_id = CD.description_id "
            sql_query+= "JOIN CARD_DESCRIPTION_MEDIA CDM ON G.description_id = CDM.description_id "
            sql_query+= "WHERE G.group_id = %s "
            sql_query+= "ORDER BY CD.init_time DESC "
            cursor.execute(sql_query,[group_id])
            medias = cursor.fetchall()
            try:
                media = medias[0][0]
            except Exception as e:
                media = ""
        data = {}
        data['group_name'] = user_name
        data['media'] = media
        return data
    except Exception as e:
        print ("Error Getting Group Name And Media From Group ID: "+str(e))

def get_post_info_internal(post_id):
    try:
        if not post_id:
            print("Invalid Input")
            return
        post_data = {}
        
        # card_description
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT P.user_id, CD.init_time, CD.update_time, CD.description, CD.description_id FROM POST P "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
            sql_query += "WHERE P.post_id = %s"
            cursor.execute(sql_query, [post_id])
            row = cursor.fetchall()[0]
        user_id = row[0]
        init_time = row[1]
        update_time = row[2]
        description = row[3]
        description_id = row[4]
        
        # user description
        user_data = get_user_name_and_single_profile_pic_from_user_id_internal(user_id)
        user_name = user_data['user_name']
        profile_pic = user_data['profile_pic']

        # media
        media = get_media_from_description_id_internal(description_id)

        # reaction count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM POST_REACT "
            sql_query += "WHERE post_id = %s and reaction = 'fire'"
            cursor.execute(sql_query, [post_id])
            fire_count = cursor.fetchall()[0][0]
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM POST_REACT "
            sql_query += "WHERE post_id = %s and reaction = 'like'"
            cursor.execute(sql_query, [post_id])
            like_count = cursor.fetchall()[0][0]
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM POST_REACT "
            sql_query += "WHERE post_id = %s and reaction = 'love'"
            cursor.execute(sql_query, [post_id])
            love_count = cursor.fetchall()[0][0]

        # share count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM POST_SHARED_BY_USER "
            sql_query += "WHERE post_id = %s AND user_id = %s"
            cursor.execute(sql_query, [post_id, user_id])
            share_count = cursor.fetchall()[0][0]

        # comment count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM POST_COMMENT "
            sql_query += "WHERE post_id = %s"
            cursor.execute(sql_query, [post_id])
            comment_count = cursor.fetchall()[0][0]

        post_data['user_id'] = user_id
        post_data['user_name'] = user_name
        post_data['profile_pic'] = profile_pic
        post_data['post_id'] = post_id
        post_data['description'] = description
        post_data['init_time'] = init_time
        post_data['update_time'] = update_time
        post_data['media'] = media
        post_data['like_count'] = like_count
        post_data['love_count'] = love_count
        post_data['fire_count'] = fire_count
        post_data['share_count'] = share_count
        post_data['comment_count'] = comment_count

        return post_data
    except Exception as e:
        print(f"Error Getting Post Info: {e}")
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

def get_post_comment_id_internal(post_id):
    try:
        if not post_id:
            print("Invalid Input")
            return
        with connections['default'].cursor() as cursor:
            sql_query  = "SELECT PC.comment_id FROM POST_COMMENT PC "
            sql_query += "JOIN CARD_DESCRIPTION CD ON PC.description_id = CD.description_id "
            sql_query += "WHERE post_id =%s "
            sql_query += "ORDER BY CD.init_time DESC"
            cursor.execute(sql_query, [post_id])
            rows = cursor.fetchall()
        all_comment_id =[row[0] for row in rows]
        return all_comment_id
    except Exception as e:
        print("Error Getting Post Comment ID: "+str(e))

def get_comment_info_internal(comment_id):
    try:
        if not comment_id:
            print("Invalid Input")
            return
        comment_data = {}
        # card_description
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT PC.user_id, CD.init_time, CD.update_time, CD.description, CD.description_id FROM POST_COMMENT PC "
            sql_query += "JOIN CARD_DESCRIPTION CD ON PC.description_id = CD.description_id "
            sql_query += "WHERE PC.comment_id = %s"
            cursor.execute(sql_query, [comment_id])
            row = cursor.fetchall()[0]
        user_id = row[0]
        init_time = row[1]
        update_time = row[2]
        description = row[3]
        description_id = row[4]

        # user description
        user_data = get_user_name_and_single_profile_pic_from_user_id_internal(user_id)
        user_name = user_data['user_name']
        profile_pic = user_data['profile_pic']

        # media
        media = get_media_from_description_id_internal(description_id)

        # reaction count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM COMMENT_REACT "
            sql_query += "WHERE comment_id = %s "
            cursor.execute(sql_query, [comment_id])
            react_count = cursor.fetchall()[0][0]
        
        
        # reply count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM POST_COMMENT "
            sql_query += "WHERE comment_id = %s"
            cursor.execute(sql_query, [comment_id])
            reply_count = cursor.fetchall()[0][0]
        
        comment_data['user_id'] = user_id
        comment_data['init_time'] = init_time
        comment_data['update_time'] = update_time
        comment_data['description'] = description
        comment_data['comment_id'] = comment_id
        comment_data['user_name'] = user_name
        comment_data['profile_pic'] = profile_pic
        comment_data['react_count'] = react_count
        comment_data['reply_count'] = reply_count
        comment_data['media'] = media
        
        return comment_data
    except Exception as e:
        print("Error Getting Comment Info: "+str(e))


def get_comment_reply_id_internal(comment_id):
    try:
        if not comment_id:
            print("Invalid Input")
            return
        with connections['default'].cursor() as cursor:
            sql_query  = "SELECT CR.reply_id FROM COMMENT_REPLY CR "
            sql_query += "JOIN CARD_DESCRIPTION CD ON CR.description_id = CD.description_id "
            sql_query += "WHERE comment_id =%s "
            sql_query += "ORDER BY CD.init_time DESC"
            cursor.execute(sql_query, [comment_id])
            rows = cursor.fetchall()
        all_reply_id =[row[0] for row in rows]
        return all_reply_id
    except Exception as e:
        print("Error Getting Comment Reply ID: "+str(e))
        return JsonResponse({'message':'error'})

def get_reply_info_internal(reply_id):
    try:
        if not reply_id:
            print("Invalid Input")
            return
        reply_data = {}
        # card_description
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT CR.user_id, CD.init_time, CD.update_time, CD.description, CD.description_id FROM COMMENT_REPLY CR "
            sql_query += "JOIN CARD_DESCRIPTION CD ON CR.description_id = CD.description_id "
            sql_query += "WHERE CR.reply_id = %s"
            cursor.execute(sql_query, [reply_id])
            row = cursor.fetchall()[0]
        user_id = row[0]
        init_time = row[1]
        update_time = row[2]
        description = row[3]
        description_id = row[4]

        # user description
        user_data = get_user_name_and_single_profile_pic_from_user_id_internal(user_id)
        user_name = user_data['user_name']
        profile_pic = user_data['profile_pic']

        # media
        media = get_media_from_description_id_internal(description_id)

        # reaction count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM REPLY_REACT "
            sql_query += "WHERE reply_id = %s "
            cursor.execute(sql_query, [reply_id])
            react_count = cursor.fetchall()[0][0]

        reply_data['user_id'] = user_id
        reply_data['init_time'] = init_time
        reply_data['update_time'] = update_time
        reply_data['description'] = description
        reply_data['user_name'] = user_name 
        reply_data['profile_pic'] = profile_pic 
        reply_data['media'] = media 
        reply_data['react_count'] = react_count
        reply_data['reply_id'] = reply_id
        
        return reply_data
    except Exception as e:
        print("Error Getting Reply Info: "+str(e))
   
@api_view(['POST'])
def homePage(request):
    try:
        user_id = request.data.get('user_id')
        if not user_id:
            print("Invalid Input")
            return
        with connections['default'].cursor() as cursor:
            sql_query  = "SELECT pid post_id FROM ( "
            sql_query += "SELECT P1.post_id pid FROM POST P1 "
            sql_query += "WHERE P1.user_id = %s UNION "
            sql_query += "SELECT P1.post_id pid FROM POST P1 "
            sql_query += "WHERE ( P1.post_of = 'user_post' "
            sql_query += "OR P1.post_of = 'coverphoto' "
            sql_query += "OR P1.post_of = 'profilepic' ) "
            sql_query += "AND P1.user_id IN ( "
            sql_query += "SELECT B1.user_id FROM BEFRIENDS B1 "
            sql_query += "WHERE B1.friend_id = %s UNION "
            sql_query += "SELECT B2.friend_id FROM BEFRIENDS B2 "
            sql_query += "WHERE B2.user_id = %s ) "
            sql_query += "UNION "
            sql_query += "SELECT P2.post_id FROM POST P2 "
            sql_query += "JOIN POST_IN_GROUP PIG1 ON P2.post_id = PIG1.post_id "
            sql_query += "WHERE PIG1.group_id IN ( "
            sql_query += "SELECT GM1.group_id FROM GROUP_MEMBERS GM1 "
            sql_query += "WHERE GM1.user_id = %s UNION "
            sql_query += "SELECT GO1.group_id FROM GROUP_OWNED GO1 "
            sql_query += "WHERE GO1.user_id = %s ) ) P2 "
            sql_query += "JOIN POST P3 ON P2.pid = P3.post_id "
            sql_query += "JOIN CARD_DESCRIPTION CD1 ON P3.description_id = CD1.description_id "
            sql_query += "ORDER BY CD1.init_time DESC "
            cursor.execute(sql_query, [user_id,user_id,user_id,user_id,user_id])
            results = cursor.fetchall()
            post_ids  = [row[0] for row in results]
        # post_ids = get_user_post_id_internal(user_id)
        post_infos = [get_post_info_internal(post_id) for post_id in post_ids]
        return Response(post_infos)
    except Exception as e:
        print("Error making home page: "+str(e))
        return Response({'error':str(e)})

@api_view(['POST'])
def signIn(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        print(email, password)
        if not email or not password:
            return JsonResponse({'error': 'Both email and password are required.'}, status=400)
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT user_id FROM USERS WHERE email = %s AND password = hash_password_function(%s)"
            cursor.execute(sql_query, [email, password])
            rows = cursor.fetchall()
        if not rows:
            return JsonResponse({'error': 'Invalid credentials.'}, status=401)
        user_id = rows[0][0]
        return Response({'user_id': user_id})
    except DatabaseError as e:
        print(e)
        return JsonResponse({'error': 'Database error occurred.'}, status=500)
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)

@api_view(['POST'])
def setUsers(request):
    try:
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        mobile_number = request.POST.get('mobile')
        birth_date = request.POST.get('birth_date')
        email = request.POST.get('email')
        try:
            profile_pic = request.FILES['profile_pic']
        except Exception:
            profile_pic = None
        try:
            cover_photo = request.FILES['cover_photo']
        except Exception:
            cover_photo = None
        if not user_name or not password or not mobile_number or not birth_date or not email:
            return  Response({"error":"Invalid Input! Fill the required fields"})
        user_id = set_user_internal(user_name, password, mobile_number, birth_date, email)
        if user_id==False:
            return Response({"error":"Please choose different email or password"})
        if profile_pic:
            set_profile_pic_internal(profile_pic, user_id)
        if cover_photo:
            set_cover_photo_internal(cover_photo, user_id)
        return JsonResponse({"message": "User created successfully"})
    except IntegrityError:
        print("error","IntegrityError")
        return Response({"error": "IntegrityError: User already exists"}, status=400)
    except DataError:
        print("error","DataError")
        return Response({"error": "DataError: Invalid data format"}, status=400)
    except Exception as e:
        print("error",str(e))
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)

@api_view(['POST'])
def set_user_post(request):
    try:
        user_id = request.POST.get('user_id')
        description = request.POST.get('description')
        try:
            uploaded_image = request.FILES['media']
        except Exception:
            uploaded_image = None
        if not description and not uploaded_image:
            return Response({"error":"Please provide a Description or Image"})
        description_id = set_card_description_internal(description)
        if uploaded_image:
            media_id = set_media_internal(uploaded_image)
            set_card_description_media_internal(description_id, media_id)
        post_id = set_post_internal(user_id, description_id, 'user_post')
        return JsonResponse({'message': 'Image uploaded successfully'})
    except DataError:
        print("error")
        return Response({"error": "DataError: Invalid data format"}, status=400)
    except Exception as e:
        print("error")
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)

@api_view(['POST'])
def get_friend_list(request):
    try:
        user_id = request.data.get('user_id')
        if not user_id:
            print("Invalid Input")
            return
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
            friend_data = get_user_name_and_single_profile_pic_from_user_id_internal(friend_id)
            media = friend_data['profile_pic']
            temp_obj = {}
            temp_obj['user_id'] = friend_id
            temp_obj['user_name'] = user_name
            temp_obj['media'] = media
            profile_data.append(temp_obj)
        return Response(profile_data)
    except Exception as e:
        print("Error Getting Friend List: "+str(e))
        return Response({'error':str(e)})

@api_view(['POST'])
def get_sent_friend_req_list(request):
    try:
        user_id = request.data.get('user_id')
        if not user_id:
            print("Invalid Input")
            return
        profile_data = []

        # friend_data
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT U.user_id, U.user_name FROM FRIEND_REQ FR "
            sql_query += "JOIN USERS U ON FR.friend_req_id = U.user_id "
            sql_query += "WHERE FR.user_id = %s "
            cursor.execute(sql_query, [user_id])
            rows = cursor.fetchall()
        for row in rows:
            friend_id = row[0]
            user_name = row[1]
            friend_data = get_user_name_and_single_profile_pic_from_user_id_internal(friend_id)
            media = friend_data['profile_pic']
            temp_obj = {}
            temp_obj['user_id'] = friend_id
            temp_obj['user_name'] = user_name
            temp_obj['media'] = media
            profile_data.append(temp_obj)
        return Response(profile_data)
    except Exception as e:
        print("Error Getting Friend Request List: "+str(e))
        return Response({'error':str(e)})
@api_view(['POST'])
def get_friend_req_list(request):
    try:
        user_id = request.data.get('user_id')
        if not user_id:
            print("Invalid Input")
            return
        profile_data = []

        # friend_data
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT U.user_id, U.user_name FROM FRIEND_REQ FR "
            sql_query += "JOIN USERS U ON FR.user_id = U.user_id "
            sql_query += "WHERE FR.friend_req_id = %s "
            cursor.execute(sql_query, [user_id])
            rows = cursor.fetchall()
        for row in rows:
            friend_id = row[0]
            user_name = row[1]
            friend_data = get_user_name_and_single_profile_pic_from_user_id_internal(friend_id)
            media = friend_data['profile_pic']
            temp_obj = {}
            temp_obj['user_id'] = friend_id
            temp_obj['user_name'] = user_name
            temp_obj['media'] = media
            profile_data.append(temp_obj)
        return Response(profile_data)
    except Exception as e:
        print("Error Getting Friend Request List: "+str(e))
        return Response({'error':str(e)})

def get_user_as_member_group_id_internal(user_id, group_type):
    try:
        if not user_id:
            print("Invalid Input")
            return
        with connections['default'].cursor() as cursor:
            sql_query = 'SELECT GM.group_id FROM GROUP_MEMBERS GM '
            sql_query+= 'JOIN GROUPS G ON GM.group_id = G.group_id '
            sql_query+= 'WHERE GM.user_id = %s AND G.group_type=%s'
            cursor.execute(sql_query,[user_id, group_type])
            result = cursor.fetchall()
        group_ids = [row[0] for row in result]
        return group_ids
    except Exception as e:
        print("Error Getting User As Number Group ID: "+str(e))
        return Response({'error':str(e)})
        
def get_user_not_member_or_owner_group_id_internal(user_id, group_type):
    try:
        if not user_id:
            print("Invalid Input")
            return
        with connections['default'].cursor() as cursor:
            sql_query = 'SELECT G.group_id FROM GROUPS G '
            sql_query+= 'WHERE G.group_type = %s '
            sql_query+= 'AND %s NOT IN '
            sql_query+= '((SELECT GM.user_id FROM GROUP_MEMBERS GM WHERE G.group_id = GM.group_id) UNION '
            sql_query+= '(SELECT GO.user_id FROM GROUP_OWNED GO  WHERE G.group_id = GO.group_id))'
            cursor.execute(sql_query,[group_type, user_id])
            result = cursor.fetchall()
        group_ids = [row[0] for row in result]
        return group_ids
    except Exception as e:
        print("Error Getting User Not Owner Or Member Number Group ID: "+str(e))
        return Response({'error':str(e)})
        

def get_user_as_owner_group_id_internal(user_id, group_type):
    try:
        if not user_id:
            print("Invalid Input")
            return
        with connections['default'].cursor() as cursor:
            sql_query = 'SELECT GO.group_id FROM GROUP_OWNED GO '
            sql_query+= 'JOIN GROUPS G ON G.group_id = GO.group_id '
            sql_query+= 'WHERE GO.user_id = %s AND G.group_type=%s'
            cursor.execute(sql_query,[user_id,group_type])
            result = cursor.fetchall()
        group_ids = [row[0] for row in result]
        return group_ids
    except Exception as e:
        print("Error Getting As Owner Group ID: "+str(e))
        return Response({'error':str(e)})
        
        

def get_group_info_internal(group_id):
    try:
        if not group_id:
            print("Invalid Input")
            return
        with connections['default'].cursor() as cursor:
            sql_query  = 'SELECT G.group_name, G.group_type, G.description_id, CD.description, CD.init_time, CD.update_time, COUNT(DISTINCT GM.user_id), COUNT(DISTINCT GO.user_id) FROM GROUPS G '
            sql_query += 'JOIN CARD_DESCRIPTION CD ON G.description_id = CD.description_id '
            sql_query += 'LEFT OUTER JOIN GROUP_MEMBERS GM ON GM.group_id = G.group_id '
            sql_query += 'LEFT OUTER JOIN GROUP_OWNED GO ON GO.group_id = G.group_id '
            sql_query += 'WHERE G.group_id = %s '
            sql_query += 'GROUP BY G.group_id, G.group_type, G.group_name, G.description_id, CD.description, CD.init_time,  CD.update_time '
            cursor.execute(sql_query,[group_id])
            results = cursor.fetchall()[0]
        group_name = results[0]
        group_type = results[1]
        description_id = results[2]
        description = results[3]
        init_time = results[4]
        update_time = results[5]
        member_count = results[6]
        owner_count = results[7]
        media = get_media_from_description_id_internal(description_id)
        group_data = {}
        group_data['group_id'] = group_id
        group_data['group_type'] = group_type
        group_data['group_name'] = group_name
        group_data['media'] = media
        group_data['description'] = description
        group_data['init_time'] = init_time
        group_data['update_time'] = update_time
        group_data['member_count'] = member_count
        group_data['owner_count'] = owner_count
        return group_data
    except Exception as e:
        print("Error Getting Group Info: "+str(e))
        return Response({'error':str(e)})
        


def get_rest_groups_internal(user_id, group_type):
    if not user_id or not group_type:
            print("Invalid Input")
            return
    try:
        group_ids = get_user_not_member_or_owner_group_id_internal(user_id,group_type)
        groups_data= [get_group_info_internal(group_id) for group_id in group_ids]
        return groups_data
    except Exception as e:
        print("Error Getting Groups: "+str(e))
        return Response({'error':str(e)})
        


def get_owned_groups_internal(user_id, group_type):
    if not user_id or not group_type:
            print("Invalid Input")
            return
    try:
        group_ids = get_user_as_owner_group_id_internal(user_id,group_type)
        groups_data= [get_group_info_internal(group_id) for group_id in group_ids]
        return groups_data
    except Exception as e:
        print("Error Getting Owned Groups: "+str(e))
        return Response({'error':str(e)})
        
def get_membered_groups_internal(user_id, group_type):
    if not user_id or not group_type:
            print("Invalid Input")
            return
    try:
        group_ids = get_user_as_member_group_id_internal(user_id,group_type)
        groups_data= [get_group_info_internal(group_id) for group_id in group_ids]
        return groups_data
    except Exception as e:
        print("Error Getting Membered Groups: "+str(e))
        return Response({'error':str(e)})
        

@api_view(['POST'])
def get_groups(request):
    try:
        user_id = request.data.get('user_id')
        group_type = request.data.get('group_type')
        if not user_id or not group_type:
            print("Invalid Input")
            return
        notingroup = get_rest_groups_internal(user_id,group_type)
        memberingroup = get_membered_groups_internal(user_id,group_type)
        owneringroup = get_owned_groups_internal(user_id,group_type)
        ret = {'not_in_group':notingroup, 'member_in_group':memberingroup, 'owner_in_group':owneringroup}
        return Response(ret)
    except Exception as e:
        print("Error Getting Groups: "+str(e))
        return JsonResponse({"error":"error"})

@api_view(['POST'])
def set_group(request):
    try:
        user_id = request.POST.get('user_id')
        group_name = request.POST.get('group_name')
        description = request.POST.get('description')
        try:
            uploaded_image = request.FILES['media']
        except Exception:
            uploaded_image = None
        group_type = request.POST.get('group_type')
        description_id = set_card_description_internal(description)
        if uploaded_image:
            media_id = set_media_internal(uploaded_image)
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
    except Exception as e:
        print("Error setting group: "+str(e))
        return JsonResponse({'error':'error'})

@api_view(['POST'])
def get_chat_friend_list(request):
    try:
        user_id = request.data.get('user_id')
        if not user_id:
            print("Invalid Input")
            return
        profile_data = []

        # friend_data
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT B.user_id as id FROM BEFRIENDS B "
            sql_query += "WHERE B.friend_id = %s "
            sql_query += "AND EXISTS( "
            sql_query += "SELECT * FROM MESSAGE M "
            sql_query += "WHERE (M.sender_id = B.user_id AND M.receiver_id = B.friend_id) "
            sql_query += "OR (M.receiver_id = B.user_id AND M.sender_id = B.friend_id) "
            sql_query += ") "
            sql_query += "UNION "
            sql_query += "SELECT B.friend_id as id FROM BEFRIENDS B "
            sql_query += "WHERE B.user_id = %s "
            sql_query += "AND EXISTS( "
            sql_query += "SELECT * FROM MESSAGE M "
            sql_query += "WHERE (M.sender_id = B.user_id AND M.receiver_id = B.friend_id) "
            sql_query += "OR (M.receiver_id = B.user_id AND M.sender_id = B.friend_id) "
            sql_query += ") "
            cursor.execute(sql_query, [user_id, user_id])
            rows = cursor.fetchall()
        for row in rows:
            friend_id = row[0]
            friend_data = get_user_name_and_single_profile_pic_from_user_id_internal(friend_id)
            user_name = friend_data['user_name']
            media = friend_data['profile_pic']
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
                temp_obj = {}
                temp_obj['user_id'] = friend_id
                temp_obj['user_name'] = user_name
                temp_obj['media'] = media
                temp_obj['last_message'] = last_message
                temp_obj['last_message_time'] = last_message_time
                profile_data.append(temp_obj)
        return Response(profile_data)
    except Exception as e:
        print("error")
        return Response({'error':str(e)})

@api_view(['POST'])
def get_events(request):
    try:
        print(1)
        user_id = request.data.get('user_id')
        group_type = 'event'
        notingroup = get_rest_groups_internal(user_id,group_type)
        memberingroup = get_membered_groups_internal(user_id,group_type)
        owneringroup = get_owned_groups_internal(user_id,group_type)
        notinevent = []
        print(2)
        for event in notingroup:
            group_id=event['group_id']
            with connections['default'].cursor() as cursor:
                sql_query="SELECT E.event_id, E.start_time, E.end_time, E.location FROM EVENTS E WHERE E.group_id = %s"
                cursor.execute(sql_query,[group_id])
                event_temp_info = cursor.fetchall()[0]
                event_id = event_temp_info[0]
                start_time = event_temp_info[1]
                end_time = event_temp_info[2]
                location = event_temp_info[3]
                tempnotinevent = get_group_info_internal(group_id)
                tempnotinevent['event_id'] = event_id
                tempnotinevent['start_time'] = start_time
                tempnotinevent['end_time'] = end_time
                tempnotinevent['location'] = location
                tempnotinevent['event_name'] = event['group_name']
                tempnotinevent['media'] = event['media']
                tempnotinevent['description'] = event['description']
                tempnotinevent['init_time'] = event['init_time']
                tempnotinevent['update_time'] = event['update_time']
                notinevent.append(tempnotinevent)
        ownerinevent = []
        for event in owneringroup:
            group_id=event['group_id']
            with connections['default'].cursor() as cursor:
                sql_query="SELECT E.event_id, E.start_time, E.end_time, E.location FROM EVENTS E WHERE E.group_id = %s"
                cursor.execute(sql_query,[group_id])
                event_temp_info = cursor.fetchall()[0]
                event_id = event_temp_info[0]
                start_time = event_temp_info[1]
                end_time = event_temp_info[2]
                location = event_temp_info[3]
                tempownerinevent = get_group_info_internal(group_id)
                tempownerinevent['event_id'] = event_id
                tempownerinevent['start_time'] = start_time
                tempownerinevent['end_time'] = end_time
                tempownerinevent['location'] = location
                tempownerinevent['event_name'] = event['group_name']
                tempownerinevent['media'] = event['media']
                tempownerinevent['description'] = event['description']
                tempownerinevent['init_time'] = event['init_time']
                tempownerinevent['update_time'] = event['update_time']
                ownerinevent.append(tempownerinevent)
        memberinevent = []
        for event in memberingroup:
            group_id=event['group_id']
            with connections['default'].cursor() as cursor:
                sql_query="SELECT E.event_id, E.start_time, E.end_time, E.location FROM EVENTS E WHERE E.group_id = %s"
                cursor.execute(sql_query,[group_id])
                event_temp_info = cursor.fetchall()[0]
                event_id = event_temp_info[0]
                start_time = event_temp_info[1]
                end_time = event_temp_info[2]
                location = event_temp_info[3]
                tempmemberinevent = get_group_info_internal(group_id)
                tempmemberinevent['event_id'] = event_id
                tempmemberinevent['start_time'] = start_time
                tempmemberinevent['end_time'] = end_time
                tempmemberinevent['location'] = location
                tempmemberinevent['event_name'] = event['group_name']
                tempmemberinevent['media'] = event['media']
                tempmemberinevent['description'] = event['description']
                tempmemberinevent['init_time'] = event['init_time']
                tempmemberinevent['update_time'] = event['update_time']
                memberinevent.append(tempmemberinevent)

        groups_data={'not_in_event':notinevent,'member_in_event':memberinevent,'owner_in_event':ownerinevent}
        return Response(groups_data)
    except Exception as e:
        print("Error Getting Events: "+str(e))
        return Response({'error':str(e)})

def get_event_info(group_id):
    try:
        event_info = get_group_info_internal(group_id)
        with connections['default'].cursor() as cursor:
            sql_query="SELECT E.event_id, E.start_time, E.end_time, E.location FROM EVENTS E WHERE E.group_id = %s"
            cursor.execute(sql_query,[group_id])
            event_temp_info = cursor.fetchall()
            event_id = event_temp_info[0]
            start_time = event_temp_info[1]
            end_time = event_temp_info[2]
            location = event_temp_info[3]
            event_info['event_id'] = event_id
            event_info['start_time'] = start_time
            event_info['end_time'] = end_time
            event_info['location'] = location
        return event_info
    except Exception as e:
        print("error")
        return Response({'error':str(e)})

@api_view(['POST'])
def set_event(request):
    try:
        user_id = request.POST.get('user_id')
        event_name = request.POST.get('event_name')
        description = request.POST.get('description')
        try:
            uploaded_image = request.FILES['media']
        except Exception:
            uploaded_image = None
        group_type = 'event'
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location')
        description_id = set_card_description_internal(description)
        if uploaded_image:
            media_id = set_media_internal(uploaded_image)
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
    except Exception as e:
        print("Error Setting Event: "+str(e))
        return Response({'error':str(e)})

@api_view(['POST'])
def search_users(request):
    try:
        query = request.data.get('key')
        sql_query = 'SELECT U.user_id, U.user_name FROM users U WHERE LOWER(user_name) LIKE %s'
        with connections['default'].cursor() as cursor:
            cursor.execute(sql_query, ['%' + str(query).lower() + '%'])
            results = cursor.fetchall()
            # serialized_results = [{"id": user_id, "user_name": user_name} for user_id, user_name in results]
        serialized_results = []
        for row in results:
            with connections['default'].cursor() as cursor:
                user_id = row[0]
                user_name = row[1]
                mediadata = get_user_name_and_single_profile_pic_from_user_id_internal(user_id)
                if mediadata:
                    media = mediadata['profile_pic']
                else:
                    media = ""
                temp_obj = {}
                temp_obj['profile_pic'] = media
                temp_obj['user_name'] = user_name
                temp_obj['user_id'] = user_id
                serialized_results.append(temp_obj)
        return Response(serialized_results)
    except Exception as e:
        print("Error Searching Users: "+str(e))
        return Response({'error':str(e)})

@api_view(['POST'])
def search_groups(request):
    try:
        query = request.data.get('key')
        sql_query = 'SELECT G.group_id, G.group_name, G.group_type FROM GROUPS G WHERE LOWER(G.group_name) LIKE %s'
        with connections['default'].cursor() as cursor:
            cursor.execute(sql_query, ['%' + str(query).lower() + '%'])
            results = cursor.fetchall()
            # serialized_results = [{"id": user_id, "user_name": user_name} for user_id, user_name in results]
        serialized_results = []
        for row in results:
            with connections['default'].cursor() as cursor:
                group_id = row[0]
                group_name = row[1]
                group_type = row[2]
                print('hello world')
                mediadata = get_group_name_and_single_media_from_group_id_internal(group_id)
                print("worked?")
                if mediadata['media']:
                    media = mediadata['media']
                else:
                    media = ""
                temp_obj = {}
                temp_obj['media'] = media
                temp_obj['group_name'] = group_name
                temp_obj['group_id'] = group_id
                temp_obj['group_type'] = group_type
                serialized_results.append(temp_obj)
        return Response(serialized_results)
    except Exception as e:
        print("Error Searching Groups: "+str(e))
        return Response({'error':str(e)})

@api_view(['POST'])
def get_marketplace(request):
    try:
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

            profile_pic = get_user_name_and_single_profile_pic_from_user_id_internal(user_id)['profile_pic']

            media = get_media_from_description_id_internal(description_id)
            
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
            

        return Response(posts)
    except Exception as e:
        print("Error Getting Marketplace")
        return Response({'error':str(e)})

@api_view(['POST'])
def set_marketplace(request):
    try:
        user_id = request.POST.get('user_id')
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        try:
            uploaded_image = request.FILES['media']
        except Exception:
            uploaded_image = None
        post_type = 'market'
        description_id = set_card_description_internal(description)
        if uploaded_image:
            media_id = set_media_internal(uploaded_image)
            set_card_description_media_internal(description_id, media_id)
        post_id = set_post_internal(user_id, description_id, post_type)
        with connections['default'].cursor() as cursor:
            marketplace_id_obj = cursor.var(int)
            sql_query = "INSERT INTO MARKETPLACE (PRODUCT_NAME, PRICE, POST_ID ) VALUES (%s, %s, %s) RETURNING marketplace_id INTO %s"
            cursor.execute(sql_query, [product_name, price, post_id, marketplace_id_obj])
            marketplace_id = marketplace_id_obj.getvalue()[0]
        
        return JsonResponse({'message': 'Image uploaded successfully'})
    except Exception as e:
        print("Error Setting Marketplace: "+str(e))
        return Response({'error':str(e)})

@api_view(['POST'])
def get_user_profile(request):
    try:
        user_id = request.data.get('user_id')
        profile_data = {}
        # profile_pic
        with connections['default'].cursor() as cursor:
            profiles = get_user_name_and_profile_pic_from_user_id_internal(user_id)
            profile_pic = profiles['profile_pic']
            user_name = profiles['user_name']
            profile_data['profile_pic'] =  profile_pic
        # cover_photo
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT create_media_url(CDM.media_id) FROM USERS U "
            sql_query += "JOIN USER_COVER_PHOTO UCP ON U.user_id = UCP.user_id "
            sql_query += "JOIN POST P ON UCP.post_id = P.post_id "
            sql_query += "JOIN CARD_DESCRIPTION CD ON P.description_id = CD.description_id "
            sql_query += "JOIN CARD_DESCRIPTION_MEDIA CDM ON CD.description_id = CDM.description_id "
            sql_query += "WHERE U.user_id = %s "
            sql_query += "ORDER BY CDM.media_id DESC"
            cursor.execute(sql_query, [user_id])
            cover_photos = cursor.fetchall()
            cover_photo = []
            for row in cover_photos:
                cover_photo.append(row[0])
            profile_data['cover_photo'] = cover_photo

        # friends count
        with connections['default'].cursor() as cursor:
            sql_query =  "SELECT COUNT(*) FROM BEFRIENDS "
            sql_query += "WHERE user_id = %s "
            sql_query += "OR friend_id = %s"
            cursor.execute(sql_query, [user_id, user_id])
            friend_count = cursor.fetchall()[0]
            profile_data['friend_count'] = friend_count[0]
            profile_data['user_id'] = user_id

        return Response(profile_data)
    except Exception as e:
        print("error")
        return Response({'error':str(e)})

@api_view(['POST'])
def get_comment_info(request):
    try:
        post_id = request.data.get('post_id')
        comment_ids = get_post_comment_id_internal(post_id)
        
        comment_data = [get_comment_info_internal(comment_id) for comment_id in comment_ids]
        
        return Response(comment_data)
    except Exception as e:
        print("error")
        return Response({'error':str(e)})

@api_view(['POST'])
def get_reply_info(request):
    try:
        comment_id = request.data.get('comment_id')
        reply_ids = get_comment_reply_id_internal(comment_id)
        
        reply_data = []
        for reply_id in reply_ids:
            reply_info = get_reply_info_internal(reply_id)
            reply_data.append(reply_info)
        
        return Response(reply_data)
    except Exception as e:
        print("error")
        return Response({'error':str(e)})

@api_view(['POST'])
def set_post_comment(request):
    try:
        user_id = request.POST.get('user_id')
        description = request.POST.get('description')
        post_id = request.POST.get('post_id')
        try:
            uploaded_image = request.FILES['media']
        except Exception:
            uploaded_image = None
        if not user_id or (not description and not uploaded_image):
            return Response({"error":"Insufficient Info"})
        
        description_id = set_card_description_internal(description)
        if uploaded_image:
            media_id = set_media_internal(uploaded_image)
            set_card_description_media_internal(description_id, media_id)

        with connections['default'].cursor() as cursor:
            post_comment_id_obj = cursor.var(int)
            sql_query = "INSERT INTO POST_COMMENT (user_id, description_id, post_id) VALUES (%s, %s, %s) RETURNING comment_id INTO %s"
            cursor.execute(sql_query, [user_id, description_id, post_id, post_comment_id_obj])
            comment_id = post_comment_id_obj.getvalue()[0]
        return Response({"message":"success"})
    except  Exception as e:
        print("Error Setting Post Comment: "+str(e))
        return Response({'error':str(e)})


@api_view(['POST'])
def set_comment_reply(request):
    try:
        user_id = request.POST.get('user_id')
        description = request.POST.get('description')
        comment_id = request.POST.get('comment_id')
        try:
            uploaded_image = request.FILES['media']
        except Exception:
            uploaded_image = None
        if not user_id or (not description and not uploaded_image):
            return Response({"error":"Insufficient Info"})
        
        description_id = set_card_description_internal(description)
        if uploaded_image:
            media_id = set_media_internal(uploaded_image)
            set_card_description_media_internal(description_id, media_id)

        with connections['default'].cursor() as cursor:
            reply_id_obj = cursor.var(int)
            sql_query = "INSERT INTO COMMENT_REPLY (user_id, description_id, comment_id) VALUES (%s, %s, %s) RETURNING reply_id INTO %s"
            cursor.execute(sql_query, [user_id, description_id, comment_id, reply_id_obj])
            reply_id = reply_id_obj.getvalue()[0]

        
        return JsonResponse({'message': 'Image uploaded successfully'})
    except Exception as e:
        print("Error Setting Comment Reply: "+str(e))
        return Response({'error':str(e)})

@api_view(['POST'])
def update_user_post(request):
    try:
        description = request.POST.get('description')
        post_id = request.POST.get('post_id')
        try:
            uploaded_image = request.FILES['media']
        except Exception:
            uploaded_image = None
        if not post_id or (not description and not  uploaded_image):
            return Response({"error":"Insufficient Information"})
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT CDM.media_id FROM CARD_DESCRIPTION_MEDIA CDM JOIN POST P ON CDM.description_id = P.description_id WHERE P.post_id = %s"
            cursor.execute(sql_query,[post_id])
            medias = cursor.fetchall()
            media = [row[0] for row in medias]
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT CD.description_id FROM CARD_DESCRIPTION CD JOIN POST P ON CD.description_id = P.description_id WHERE P.post_id = %s"
            cursor.execute(sql_query,[post_id])
            description_ids=cursor.fetchall()
            description_id = description_ids[0][0]
        with connections['default'].cursor() as cursor:
            sql_query = "UPDATE CARD_DESCRIPTION SET description=%s, update_time=SYSDATE WHERE description_id = %s"
            cursor.execute(sql_query,[description,description_id])
            
        if uploaded_image:
            media_id = set_media_internal(uploaded_image)
            set_card_description_media_internal(description_id, media_id)
        for media_id in media:
            with connections['default'].cursor() as cursor:
                sql_query = "DELETE FROM MEDIA WHERE media_id = %s"
                cursor.execute(sql_query, [media_id])
            delete_file(absolute_image_path+str(media_id))

        return JsonResponse({'message': 'Image uploaded successfully'})
    except IntegrityError:
        print("error")
        return Response({"error": "IntegrityError: User already exists"}, status=400)
    except DataError:
        print("error")
        return Response({"error": "DataError: Invalid data format"}, status=400)
    except Exception as e:
        print("error")
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)

def delete_user_post_internal(post_id):
    try:
        with connections['default'].cursor() as cursor:
                sql_query = "SELECT CDM.media_id FROM CARD_DESCRIPTION_MEDIA CDM JOIN POST P ON CDM.description_id = P.description_id WHERE P.post_id = %s"
                cursor.execute(sql_query,[post_id])
                medias = cursor.fetchall()
                media = [row[0] for row in medias]
        with connections['default'].cursor() as cursor:
                sql_query = "SELECT CD.description_id FROM CARD_DESCRIPTION CD JOIN POST P ON CD.description_id = P.description_id WHERE P.post_id = %s"
                cursor.execute(sql_query,[post_id])
                description_ids=cursor.fetchall()
                description_id = description_ids[0][0]
        for media_id in media:
                with connections['default'].cursor() as cursor:
                    sql_query = "DELETE FROM MEDIA WHERE media_id = %s"
                    cursor.execute(sql_query, [media_id])
                delete_file(absolute_image_path+str(media_id))
        with  connections['default'].cursor() as cursor:
            sql_query = "DELETE FROM CARD_DESCRIPTION WHERE description_id = %s"
            cursor.execute(sql_query, [description_id])
        return JsonResponse({"message":"success"})
    except Exception as e:
        print("Error Deleting User Post: "+str(e))
        return Response({'error':str(e)})

@api_view(['POST'])
def delete_user_post(request):
    try:
        post_id = request.data.get('post_id')
        return delete_user_post_internal(post_id)
    except Exception as e:
        print("Error Deleting User Post: "+str(e))
        return Response({'error':str(e)})

def get_user_name_and_profile_pic_from_user_id_internal(user_id):
    try:
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT user_name FROM USERS "
            sql_query+= "WHERE user_id = %s "
            cursor.execute(sql_query,[user_id])
            user_name = cursor.fetchall()[0][0]
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT create_media_url(CDM.media_id) FROM USER_PROFILE_PIC UPP "
            sql_query+= "JOIN POST P ON UPP.post_id = P.post_id "
            sql_query+= "JOIN CARD_DESCRIPTION_MEDIA CDM ON P.description_id = CDM.description_id "
            sql_query+= "WHERE UPP.user_id = %s "
            cursor.execute(sql_query,[user_id])
            medias = cursor.fetchall()
            media = [row[0] for row in medias]
        data = {}
        data['user_name'] = user_name
        data['profile_pic'] = media
        return data
    except Exception as e:
        print ("Error Getting User Name And Profile Pic From User ID: "+str(e))
        return Response({'error':str(e)})

def get_media_from_description_id_internal(description_id):
    try:
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT create_media_url(CDM.media_id) FROM CARD_DESCRIPTION_MEDIA CDM "
            sql_query+= "WHERE CDM.description_id = %s "
            cursor.execute(sql_query,[description_id])
            medias = cursor.fetchall()
            media = [row[0] for row in medias]
        return media
    except Exception as e:
        print("Error Getting Media From Description ID: "+str(e))
        return Response({'error':str(e)})
    

@api_view(['POST'])
def get_messages(request):
    try:
        user_id = request.data.get('user_id')
        friend_id = request.data.get('friend_id')
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT M.sender_id, M.receiver_id, CD.description, CD.init_time, CD.description_id FROM MESSAGE M "
            sql_query+= "JOIN CARD_DESCRIPTION CD ON M.description_id = CD.description_id "
            sql_query+= "WHERE M.sender_id = %s AND M.receiver_id = %s "
            sql_query+= "OR M.sender_id = %s AND M.receiver_id = %s "
            sql_query+= "ORDER BY CD.init_time DESC "
            cursor.execute(sql_query,[user_id,friend_id,friend_id,user_id])
            results = cursor.fetchall()
        message_info = []
        for result in results:
            sender_id = result[0]
            receiver_id = result[1]
            description = result[2]
            init_time = result[3]
            description_id = result[4]
            sender_data = get_user_name_and_single_profile_pic_from_user_id_internal(sender_id)
            receiver_data = get_user_name_and_single_profile_pic_from_user_id_internal(receiver_id)
            media = get_media_from_description_id_internal(description_id)
            sender_name = sender_data['user_name']
            receiver_name = receiver_data['user_name']
            sender_profile_pic = sender_data['profile_pic']
            receiver_profile_pic = receiver_data['profile_pic']
            message_data = {}
            message_data['sender_id'] = sender_id
            message_data['receiver_id'] = receiver_id
            message_data['description'] = description
            message_data['init_time'] = init_time
            message_data['sender_name'] = sender_name
            message_data['receiver_name'] = receiver_name
            message_data['sender_profile_pic'] = sender_profile_pic
            message_data['receiver_profile_pic'] = receiver_profile_pic
            message_data['media'] = media
            message_info.append(message_data)
        return Response(message_info)
    except Exception  as e:
        print("Error Getting Message: "+str(e))
        return Response({'error':str(e)})
        
@api_view(['POST'])
def set_message(request):
    try:
        user_id = request.POST.get('user_id')
        friend_id = request.POST.get('friend_id')
        description = request.POST.get('description')
        try:
            uploaded_image = request.FILES['media']
        except Exception:
            uploaded_image = None
        print(user_id,friend_id)
        if not user_id and not friend_id:
            print("Invalid Input")
            return Response({"error":"invalid input"})
        if not description:
            description=""
        
        description_id = set_card_description_internal(description)
        if uploaded_image:
            media_id = set_media_internal(uploaded_image)
            set_card_description_media_internal(description_id, media_id)

        with connections['default'].cursor() as cursor:
            message_id_obj = cursor.var(int)
            sql_query = "INSERT INTO MESSAGE (sender_id, receiver_id, description_id) VALUES (%s, %s, %s) RETURNING message_id INTO %s"
            cursor.execute(sql_query, [user_id, friend_id, description_id, message_id_obj])
            message_id = message_id_obj.getvalue()[0]

        
        return JsonResponse({'message': 'Image uploaded successfully'})
    except Exception as e:
        print("Error Setting Message: "+str(e))
        return Response({'error':str(e)})

def get_group_post_ids_internal(group_id):
    try:
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT * FROM POST_IN_GROUP PIG WHERE PIG.group_id = %s"
            cursor.execute(sql_query,[group_id])
            results = cursor.fetchall()
        ret = [row[0] for row in results]
        return ret
    except Exception as e:
        print("error")
        return Response({'error':str(e)})

def get_group_post_info_internal(group_id):
    try:
        post_ids = get_group_post_ids_internal(group_id)
        post_info = [get_post_info_internal(post_id) for post_id in post_ids]
        return post_info
    except Exception as e:
        print("error")
        return Response({'error':str(e)})

@api_view(['POST'])
def get_group_page(request):
    try:
        group_id = request.data.get('group_id')
        group_info = get_group_info_internal(group_id)
        post_info = get_group_post_info_internal(group_id)
        return Response({'group_info':group_info, 'post_info':post_info})
    except Exception as e:
        print("error")
        return Response({'error':str(e)})

@api_view(['POST'])
def set_group_post(request):
    try:
        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')
        description = request.POST.get('description')
        try:
            uploaded_image = request.FILES['media']
        except Exception:
            uploaded_image = None
        description_id = set_card_description_internal(description)
        if uploaded_image:
            media_id = set_media_internal(uploaded_image)
            set_card_description_media_internal(description_id, media_id)
        post_id = set_post_internal(user_id, description_id, 'group_post')
        with connections['default'].cursor() as cursor:
            sql_query = "INSERT INTO POST_IN_GROUP (post_id, group_id) VALUES (%s,%s)"
            cursor.execute(sql_query,[post_id,group_id])
        return JsonResponse({'message': 'Image uploaded successfully'})
    except IntegrityError:
        print("error")
        return Response({"error": "IntegrityError: User already exists"}, status=400)
    except DataError:
        print("error")
        return Response({"error": "DataError: Invalid data format"}, status=400)
    except Exception as e:
        print("error")
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)
    
@api_view(['POST'])
def is_friend(request):
    try:
        user_id = request.data.get('user_id')
        friend_id = request.data.get('friend_id')
        print(user_id,friend_id)
        if int(user_id) == int(friend_id):
            print("worked?")
            return Response({"status":"own"})
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT COUNT(*) FROM BEFRIENDS WHERE (user_id = %s AND friend_id = %s) OR (user_id = %s AND friend_id = %s)"
            cursor.execute(sql_query, [user_id, friend_id, friend_id, user_id])
            friend = cursor.fetchall()[0][0]
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT COUNT(*) FROM FRIEND_REQ WHERE user_id = %s AND friend_req_id = %s"
            cursor.execute(sql_query, [user_id, friend_id])
            sent_request = cursor.fetchall()[0][0]
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT COUNT(*) FROM FRIEND_REQ WHERE user_id = %s AND friend_req_id = %s"
            cursor.execute(sql_query, [friend_id, user_id])
            received_request = cursor.fetchall()[0][0]
        if int(friend)>0:
            return Response({"status":"friend"})
        if int(sent_request)>0:
            return Response({"status":"sent"})
        if int(received_request)>0:
            return Response({"status":"received"})
        return Response({"status":"none"})
    except Exception as e:
        print("error")
        return Response({'error':str(e)})

@api_view(['POST'])
def delete_user(request):
    try:
        user_id = request.data.get('user_id')
        with connections['default'].cursor() as cursor:
            sql_query = "DELETE FROM USERS WHERE user_id = %s"
            cursor.execute(sql_query,[user_id])
        return Response({"success":"success"})
    except Exception as e:
        print("error")
        return Response({'error':str(e)})

@api_view(['POST'])
def unfriend(request):
    try:
        user_id = request.data.get('user_id')
        friend_id = request.data.get('friend_id')
        with connections['default'].cursor() as cursor:
            sql_query = "DELETE FROM BEFRIENDS WHERE (user_id=%s AND friend_id=%s) OR (user_id=%s AND friend_id=%s)"
            cursor.execute(sql_query,[user_id,friend_id,friend_id,user_id])
        return Response({"success":"success"})
    except Exception as e:
        print("error")
        return Response({'error':str(e)})

@api_view(['POST'])
def delete_request(request):
    try:
        user_id = request.data.get('user_id')
        friend_id = request.data.get('friend_id')
        with connections['default'].cursor() as cursor:
            sql_query = "DELETE FROM FRIEND_REQ WHERE (user_id=%s AND friend_req_id=%s) OR (user_id=%s AND friend_req_id=%s)"
            cursor.execute(sql_query,[user_id,friend_id,friend_id,user_id])
        return Response({"success":"success"})
    except Exception as e:
        print("error")
        return Response({'error':str(e)})

@api_view(['POST'])
def send_request(request):
    try:
        user_id = request.data.get('user_id')
        friend_id = request.data.get('friend_id')
        with connections['default'].cursor() as cursor:
            sql_query = "INSERT INTO FRIEND_REQ (user_id,friend_req_id) VALUES (%s,%s) "
            cursor.execute(sql_query,[user_id,friend_id])
        return Response({"success":"success"})
    except Exception as e:
        print("Error",e)
        return Response({'error':str(e)})

@api_view(['POST'])
def accept_request(request):
    try:
        user_id = request.data.get('user_id')
        friend_id = request.data.get('friend_id')
        sql_query = 'BEGIN '
        sql_query+= 'accept_friend_req(p_friend_req_id => %s, p_user_id => %s); '
        sql_query+= 'END;/'
        with connections['default'].cursor() as cursor:
            cursor.execute(sql_query,[friend_id,user_id])
        return Response({"success":"success"})
    except Exception as e:
        print("Error",e)
        return Response({'error':str(e)})

@api_view(['POST'])
def is_in_group(request):
    try:
        user_id = request.data.get('user_id')
        group_id = request.data.get('group_id')
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT COUNT(*) FROM GROUP_MEMBERS WHERE group_id=%s AND user_id=%s"
            cursor.execute(sql_query,[group_id,user_id])
            member=int(cursor.fetchall()[0][0])
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT COUNT(*) FROM GROUP_OWNED WHERE group_id=%s AND user_id=%s"
            cursor.execute(sql_query,[group_id,user_id])
            owner=int(cursor.fetchall()[0][0])
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT COUNT(*) FROM GROUP_REQUESTED WHERE group_id=%s AND user_id=%s"
            cursor.execute(sql_query,[group_id,user_id])
            requested=int(cursor.fetchall()[0][0])
        if owner>0:
            return Response({"status":"owner"})
        if member>0:
            return Response({"status":"member"})
        if requested>0:
            return Response({"status":"requested"})
        return Response({"status":"none"})
    except Exception as e:
        print("Error",e)
        return Response({'error':str(e)})

@api_view(['POST'])
def delete_group(request):
    try:
        group_id = request.data.get('group_id')
        post_ids = get_group_post_ids_internal(group_id)
        with connections['default'].cursor() as cursor:
            sql_query = "DELETE FROM GROUPS WHERE group_id = %s"
            cursor.execute(sql_query,[group_id])
        for post_id in post_ids:
            delete_user_post_internal(post_id)
        return Response({"message":"success"})
    except Exception as e:
        print("Error",e)
        return Response({'error':str(e)})

@api_view(['POST'])
def group_reqs(request):
    try:
        group_id = request.data.get('group_id')
        with connections['default'].cursor() as cursor:
            sql_query = "SELECT user_id FROM GROUP_REQUESTED WHERE group_id = %s"
            cursor.execute(sql_query,[group_id])
            result = cursor.fetchall()
        data = [get_user_name_and_single_profile_pic_from_user_id_internal(user_id[0]) for user_id in result]
        return Response(data)
    except Exception as e:
        print("Error",e)
        return Response({'error':str(e)})

@api_view(['POST'])
def send_req_in_group(request):
    try:
        group_id = request.data.get('group_id')
        user_id = request.data.get('user_id')
        with connections['default'].cursor() as cursor:
            sql_query = "INSERT INTO GROUP_REQUESTED(group_id,user_id) VALUES (%s,%s)"
            cursor.execute(sql_query,[group_id,user_id])
        return Response({"message":"success"})
    except Exception as e:
        print("Error",e)
        return Response({'error':str(e)})

@api_view(['POST'])
def accept_req_in_group(request):
    try:
        group_id = request.data.get('group_id')
        user_id = request.data.get('user_id')
        sql_query = 'DECLARE '
        sql_query+= 'v_result VARCHAR2(100); '
        sql_query+= 'BEGIN '
        sql_query+= 'accept_req_in_group(p_group_id => %s, p_user_id => %s); '
        sql_query+= 'END;/'
        with connections['default'].cursor() as cursor:
            cursor.execute(sql_query,[group_id,user_id])

        return Response({"message":"success"})
    except Exception as e:
        print("Error",e)
        return Response({'error':str(e)})

@api_view(['POST'])
def reject_req_in_group(request):
    try:
        group_id = request.data.get('group_id')
        user_id = request.data.get('user_id')
        with connections['default'].cursor() as cursor:
            sql_query = "DELETE FROM GROUP_REQUESTED WHERE group_id=%s AND user_id=%s"
            cursor.execute(sql_query,[group_id,user_id])
        return Response({"message":"success"})
    except Exception as e:
        print("Error",e)
        return Response({'error':str(e)})

@api_view(['POST'])
def leave_from_group(request):
    try:
        group_id = request.data.get('group_id')
        user_id = request.data.get('user_id')
        with connections['default'].cursor() as cursor:
            sql_query = "DELETE FROM GROUP_MEMBERS WHERE group_id=%s AND user_id=%s"
            cursor.execute(sql_query,[group_id,user_id])
        return Response({"message":"success"})
    except Exception as e:
        print("Error",e)
        return Response({'error':str(e)})

@api_view(['POST'])
def add_post_react(request):
    try:
        post_id = request.data.get('post_id')
        user_id = request.data.get('user_id')
        reaction = request.data.get('reaction')
        sql_query = 'BEGIN '
        sql_query+= 'INSERT_OR_UPDATE_POST_REACT(p_post_id => %s, p_user_id => %s, p_reaction => %s); '
        sql_query+= 'END;/'
        with connections['default'].cursor() as cursor:
            print("hello")
            cursor.execute(sql_query,[post_id,user_id,reaction])
            print("world")
        return JsonResponse({"success":"success"})
    except Exception as e:
        print("Error",e)
        return Response({'error':str(e)})
    # react