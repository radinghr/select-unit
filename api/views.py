from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.forms.models import model_to_dict
from rest_framework.authentication import get_authorization_header
from . import utils
from .models import User, Major, Course, StudentCourse
from .serializer import ProfileSerializer, LoginSerializer, AddMajorSerializer
from .http_response import bad_request_response, success_response, not_found_response, not_acceptable_response, \
    error_response, un_auth_response
import json
from api.jwt_utils import create_jwt_token, extract_jwt_payload
from select_unit.mixins import GeneralClassMixin
from api.function_utils import get_token


# Create your views here.


class GenericUser(GeneralClassMixin):
    serializer_class = ProfileSerializer
    name = "User"

    def post(self, request):
        post_params = json.loads(request.body.decode('utf-8'))
        username = post_params.get("email")
        password = post_params.get("password")
        semester = int(post_params.get("semester", 1))
        major_id = int(post_params.get("major_id", 0))
        full_name = post_params.get("full_name")
        student_number = post_params.get("student_number", 0)

        for i in [username, password, semester, major_id, full_name, student_number]:
            if i is None or i is 0:
                return bad_request_response(
                    message="Request must contain email, password, semester, major_id, full_name and student_number",
                    code=400)

        major_obj = Major.objects.filter(id=major_id)
        if bool(major_obj):
            try:
                user = User.objects.create(username=username, semester=semester, major=major_obj[0],
                                           full_name=full_name, is_normal_user=1, is_staff=0,
                                           is_superuser=0, student_number=student_number)
                user.set_password(password)
                user.save()
                token = create_jwt_token(user)
                content = {'token': str(token)}
                return success_response(data=content)
            except Exception as e:
                print(str(e))
                return error_response(utils.DATABASE_ERROR)
        else:
            return error_response(utils.MAJOR_NOT_FOUND)

    def get(self, request):
        username, err = get_token(request)
        print(username, err)
        if err is not None:
            print(err)
            return un_auth_response(message="Bad or missing token.")
        try:
            user_obj = User.objects.get(username=username)
            data = {
                "email": user_obj.username,
                "full_name": user_obj.full_name,
                "student_number": user_obj.student_number,
                "semester": user_obj.semester,
                "major": Major.objects.get(id=user_obj.major_id).name
            }
            return success_response(data=data)
        except Exception as e:
            print(e)
            return error_response(utils.USER_NOT_FOUND)

    def put(self, request):
        username, err = get_token(request)
        if err is not None:
            return un_auth_response(message="Bad or missing token.")

        post_params = json.loads(request.body.decode('utf-8'))
        semester = int(post_params.get("semester", 1))
        major_id = int(post_params.get("major_id", 0))
        full_name = post_params.get("full_name")
        student_number = post_params.get("student_number", 0)

        for i in [semester, major_id, full_name, student_number]:
            if i is None or i is 0:
                return bad_request_response(
                    message="Request must contain semester, major_id, full_name and student_number",
                    code=400)

        major_obj = Major.objects.filter(id=major_id)
        if bool(major_obj):
            try:
                user = User.objects.get(username=username)
                user.semester = int(semester)
                user.major = major_obj[0]
                user.student_number = student_number
                user.full_name = full_name
                user.save()
                token = create_jwt_token(user)
                content = {'token': str(token)}
                return success_response(data=content)
            except Exception as e:
                print(str(e))
                return error_response(utils.USER_NOT_FOUND)
        else:
            return error_response(utils.MAJOR_NOT_FOUND)


class UserChangePassword(GeneralClassMixin):
    name = "UserChangePassword"

    def put(self, request):
        username, err = get_token(request)
        if err is not None:
            return un_auth_response(message="Bad or missing token.")

        post_params = json.loads(request.body.decode('utf-8'))
        old_password = post_params.get("old_password")
        new_password = post_params.get("new_password")
        for i in [old_password, new_password]:
            if i is None or i is 0:
                return bad_request_response(
                    message="Request must contain old_password, new_password.",
                    code=400)

        user = authenticate(username=username, password=old_password)
        if user:
            if user.is_normal_user and user.is_active:
                login(request, user)
                try:
                    user_obj = User.objects.get(username=username)
                    user_obj.set_password(new_password)
                    user_obj.save()
                    user_token = create_jwt_token(user)
                    content = {'token': str(user_token)}
                    return success_response(content)
                except Exception as e:
                    print(str(e))
                    return error_response(utils.USER_NOT_FOUND)
        return un_auth_response(code=403)


class CheckUserRegisterEmail(GeneralClassMixin):
    name = "CheckUserEmailRegister"

    def post(self, request):
        post_params = json.loads(request.body.decode('utf-8'))
        username = post_params.get("email")
        if User.objects.filter(username=username).exists():
            content = "This username already exists."
            return bad_request_response(message=content, code=400)

        else:
            content = {'messsage': 'You can create user with this email!'}
            return success_response(data=content)


class LoginUser(GeneralClassMixin):
    serializer_class = LoginSerializer
    name = 'UserLogin'

    def post(self, request):
        post_params = json.loads(request.body.decode('utf-8'))
        username = post_params.get("email")
        password = post_params.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_normal_user and user.is_active:
                login(request, user)
                user_token = create_jwt_token(user)
                content = {'token': str(user_token)}
                return success_response(content)
        return un_auth_response(code=403)


class MajorList(GeneralClassMixin):
    name = "MajorList"

    def get(self, request):
        major_all_obj = Major.objects.all()
        major_list = list()

        for obj in major_all_obj:
            major_list.append(model_to_dict(obj))
        return success_response(major_list)


class AddMajor(GeneralClassMixin):
    name = "MajorAdd"
    serializer_class = AddMajorSerializer

    def post(self, request):
        post_params = json.loads(request.body.decode('utf-8'))
        major_name = post_params.get('name')
        major_obj = Major.objects.create(name=major_name)
        data = model_to_dict(major_obj)
        return success_response({'object': data})


class GenericCourse(GeneralClassMixin):
    name = "Course"

    def get(self, request):
        username, err = get_token(request)
        if err is not None:
            return un_auth_response(message="Bad or missing token.")

        query_params = ["name", "teacher_name", "exam_time", "exam_day", "type", "semester",
                        "capacity", "register_id"]
        q_objects = Q()
        for queue in query_params:
            value = request.GET.get(queue)
            if value is not None:
                q_objects |= Q(**{queue: value})

        try:
            courses = Course.objects.filter(q_objects)
        except Exception as e:
            return bad_request_response()
        data = list()
        for obj in courses:
            obj.class_times = json.loads(obj.class_times)
            data.append(model_to_dict(obj))

        return success_response(data=data)


class UserCourse(GeneralClassMixin):
    name = "UserCourse"

    def get(self, request):
        username, err = get_token(request)
        if err is not None:
            return un_auth_response(message="Bad or missing token.")
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return error_response(utils.USER_NOT_FOUND)
        courses = StudentCourse.objects.filter(user_id=user.id)
        student_courses = list()
        if len(courses) == 0:
            return success_response(student_courses)
        q_objects = Q()
        for crs in courses:
            course_id = crs.course_id
            q_objects |= Q(register_id=course_id)
        course_obj = Course.objects.filter(q_objects)
        for obj in course_obj:
            obj.class_times = json.loads(obj.class_times)
            student_courses.append(model_to_dict(obj))
        return success_response(student_courses)

    def post(self, request):
        username, err = get_token(request)
        if err is not None:
            return un_auth_response(message="Bad or missing token.")
        post_params = json.loads(request.body.decode('utf-8'))
        # TODO Check course duplicate
        course_id = post_params.get("register_id")
        if course_id is None:
            return bad_request_response(message="Request must contain register_id.", code=400)

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return error_response(utils.USER_NOT_FOUND)
        if len(StudentCourse.objects.filter(course_id=course_id, user_id=user.id)):
            return bad_request_response("This course already exists")

        new_course = StudentCourse.objects.create(course_id=course_id, user_id=user.id)
        new_course.save()
        return success_response({"message": "Course added succesfully"})


class UserCourseDelete(GeneralClassMixin):
    name = "UserCourseDelete"

    def post(self, request):
        username, err = get_token(request)
        if err is not None:
            return un_auth_response(message="Bad or missing token.")
        post_params = json.loads(request.body.decode('utf-8'))
        course_id = post_params.get("register_id")
        if course_id is None:
            return bad_request_response(message="Request must contain register_id.", code=400)

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return error_response(utils.USER_NOT_FOUND)

        new_course = StudentCourse.objects.get(course_id=course_id, user_id=user.id)
        new_course.delete()

        return success_response({"message": "Course deleted succesfully"})


class TokenTest(GeneralClassMixin):
    name = "test"

    def post(self, request):
        token, error = get_token(request)
        print(token, error)
        return success_response("test")
