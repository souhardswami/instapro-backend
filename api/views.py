from django.shortcuts import render

from django.http import request,HttpResponse


from .serializers import UserSerializer,PhotosSerializer,CommentSerializer,LikeSerializer,TagHashSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


from main.models import Users,Photos,Connection,Comment,Like,TagHash,Tags

from rest_framework import status


from django.db import connection
# Create your views here.








class Follower(APIView):
    
    

    
    def post(self, request, format=None):

        
        


        userId=request.data['user']
        

        user=Connection.objects.filter(user=userId)

        value=[]
        for i in user:
            value.append(i.follower.id)
        
        
        user=Users.objects.filter(id__in=value)
        
        

        serializer = UserSerializer(user,many=True)
        return Response(serializer.data)


class Following(APIView):
    
    

    
    def post(self, request, format=None):
        

        userId=request.data['user']
        


        user=Connection.objects.filter(follower=userId)

        value=[]
        for i in user:
            value.append(i.user.id)
        
        user=Users.objects.filter(id__in=value)
        
        

        serializer = UserSerializer(user,many=True)
        return Response(serializer.data)
        

        

  



class Post(APIView):
    
    

    
    def post(self, request, format=None):
        
        

        userId=request.data['user']
        


        photo=Photos.objects.filter(user__id=userId).order_by('-created_at')
        for i in photo:
            i.username=i.user.username
        

        
        
        

        serializer = PhotosSerializer(photo,many=True)
        
        return Response(serializer.data)
        

        

  

    
class userAuth(APIView):

    def post(self, request, format=None):

        

        username=request.data['username']
        
        password=request.data['password']
        

        # users={}  # in case if password or username not found
        
        # with connection.cursor() as cursor:
        
        #     cursor.execute("SELECT * FROM main_users where username=%s and password=%s",[username,password])
    
        
        #     rows = cursor.fetchall()

        #     for row in rows:
        #         print(row)
        #         users.append(list(row))
        users=Users.objects.filter(username=username,password=password)
        
        
        
        serializer = UserSerializer(users,many=True)
       


        return Response(serializer.data)


    
class userImage(APIView):

    def post(self, request, format=None):

        # photos=Photos.objects.filter(users__id=request.data['user'])
        # serializer = PhotosSerializer(photos,many=True)
        # return Response(serializer.data)

        



        # follower=list(Users.objects.filter(followers__id=request.data['user']))
        # print(follower)
        userId=request.data['user']
        user=Connection.objects.filter(user=userId)

        value=[]
        for i in user:
            value.append(i.follower.id)
        

        # follower.append(request.data['user'])
        value.append(userId)

        
        
        photos=Photos.objects.filter(user__in=value).order_by('-created_at')
        for i in photos:
            i.username=i.user.username
        
        # print(photos)
        

        
        serializer = PhotosSerializer(photos,many=True)
        
        return Response(serializer.data)



class Search(APIView):

    def post(self,request,format=None):
        

        item=request.data['item']
        from django.db.models import Q


        if(item[0]!='#'):
            user=Users.objects.filter(Q(name__contains=item) | Q(username__contains=item))
            serializer = UserSerializer(user,many=True)
        
            return Response(serializer.data)
        else:
            print(item)
            user=TagHash.objects.filter(Q(tagword__contains=item) )
            print(user)
            serializer = TagHashSerializer(user,many=True)

            print(serializer)
        
            return Response(serializer.data)
        





class TagDetail(APIView):

    def post(self,request,format=None):
        

        idd=request.data['idd']
        # print(idd)

        
        tags=Tags.objects.filter(tagpar__id=idd)
        photosId=[]
        for tag in tags:
            photosId.append(tag.photo.id)
        # print(photosId)
        
        



        photo=Photos.objects.filter(id__in=photosId)

        for i in photo:
            i.username="idk"

        # print(photo)

        serializer=PhotosSerializer(photo,many=True)
        
        return Response(serializer.data)
        






class Comments(APIView):

    def post(self,request,format=None):
        

        picId=request.data['picId']
        

        comments=Comment.objects.filter(photo__id=picId)

        for comment in comments:
            comment.username=comment.user.username
            comment.profile_img=comment.user.profile_img
        
        
        serializer=CommentSerializer(comments,many=True)
        return Response(serializer.data)


class Likes(APIView):

    def post(self,request,format=None):
        

        picId=request.data['picId']
        
        
        

        likes=Like.objects.filter(photo__id=picId)
       

        for like in likes:
            like.username=like.user.username
            like.profile_img=like.user.profile_img
        
        
        serializer=LikeSerializer(likes,many=True)
        return Response(serializer.data)


class Registor(APIView):

    def post(self,request,format=None):
        print(request.data)
        
        name=request.data['name']
        username=request.data['username']
        password=request.data['password']
        # print(name,username,password)
        
        
        new_user=Users.objects.create(name=name,username=username,password=password,profile_img="fake/31.jpg")

        new_user.save()
        return Response(data='successfullyregistor',status=status.HTTP_201_CREATED)

    def put(self,request,format=None):
        print(request.data)
        print("put")
        
        name=request.data['name']
        username=request.data['username']
        password=request.data['password']
        profile_img=request.data['profile_img']
        profile_img=profile_img[28:]
        
        
        
        new_user=Users.objects.get(name=name,username=username,password=password)
        new_user.profile_img=profile_img

        new_user.save()
        return Response(data="/media/"+profile_img,status=status.HTTP_201_CREATED)






class NewPost(APIView):

    def post(self,request,format=None):
        print(request.data)



        user=Users.objects.get(id=request.data['user'])
        image_url=request.data['image_url']

        # i have no idea how to handle this so temp method
        image_url=image_url[28:]
                
        


        
        tag=request.data['tag']
        tags=request.data['tags']
        photopost=Photos.objects.create(user=user,image_url=image_url,tag=tag)
        photopost.save()
        

        for tag in tags:

            tag='#'+tag
            res_object=TagHash.objects.filter(tagword=tag)

            if(res_object.count()<1):
                res_object=TagHash.objects.create(tagword=tag)
                res_object.save()
            
                taghased=Tags.objects.create(tagpar=res_object,photo=photopost)
                
                taghased.save()
            
            else:
                res_object=res_object[0]
                taghased=Tags.objects.create(tagpar=res_object,photo=photopost)
                
                taghased.save()


        


        return Response(data="succesfully created",status=status.HTTP_201_CREATED)
        




class NewComment(APIView):

    def post(self,request,format=None):



        


        
        

        user=Users.objects.get(id=request.data['user'])
        photo=Photos.objects.get(id=request.data['photo'])
        
        comment_text=request.data['comment_text']

        commentadd=Comment.objects.create(user=user,photo=photo,comment_text=comment_text)
        commentadd.save()


        return Response(data="comment added",status=status.HTTP_201_CREATED)






        






        return Response(data='succfully edited',status=status.HTTP_200_OK)     





class NewLike(APIView):

    def post(self,request,format=None):



        


        
        print(request)

        
        user_id=request.data['userId']
        user=Users.objects.get(id=user_id)
        img_id=request.data['imgId']
        photo=Photos.objects.get(id=img_id)
        new_like=Like.objects.create(photo=photo,user=user)
        new_like.save()
        


        return Response(data="liked added",status=status.HTTP_201_CREATED)






        






        return Response(data='succfully edited',status=status.HTTP_200_OK)     




class CheckFollower(APIView):
    def post(self,request,format=None):
        print(request.data)

        user=request.data['user']
        check=request.data['check']

        


        follow=Connection.objects.filter(user__id=check,follower__id=user)
        print(follow)
        if(len(follow)>0):
            print("yes")
            return Response(data=True,status=status.HTTP_200_OK) 
        else:
            print("no")
            return Response(data=False,status=status.HTTP_403_FORBIDDEN) 



class UnFollow(APIView):
    def post(self,request,format=None):
        print(request.data)

        user=request.data['user']
        user=Users.objects.get(id=user)
        check=request.data['check']
        check=Users.objects.get(id=check)

        


        new_follow=Connection.objects.get(user=check,follower=user)
        new_follow.delete()
        print(new_follow)
        
        return Response(data=True,status=status.HTTP_200_OK) 





class Follow(APIView):
    def post(self,request,format=None):
        print(request.data)

        user=request.data['user']
        user=Users.objects.get(id=user)
        check=request.data['check']
        check=Users.objects.get(id=check)

        


        new_follow=Connection.objects.create(user=check,follower=user)
        new_follow.save()
        print(new_follow)
        
        return Response(data=True,status=status.HTTP_200_OK) 
        

class Fake(APIView):
    def get(self,request,format=None):
        print(request)
        return Response(data="hello wolrd",status=status.HTTP_200_OK)