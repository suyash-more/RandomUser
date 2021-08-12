# rest framework imports
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# custom imports
from .serializer import RegisterSerializer
from .models import Person
import requests
import random

status_dict = {"success": {"status": "Data valid"},
               "fail": {"status": "Data invalid"}}


class RegisterView(APIView):
    # Anyone is allowed to hit this url
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # register your user for helping in growing the database at this point
    # the fields this api accept are ['first_name', 'last_name', 'age', 'birth_date', 'sex']
    def post(self, request):
        data_serializer = RegisterSerializer(data=request.data)

        # checking validity of data
        if not data_serializer.is_valid():
            return Response(status_dict.get('fail'))
        data_serializer.save()
        return Response(status_dict.get('success'))


class AutomateUserCreation(APIView):
    # Anyone is allowed to hit this URL
    permission_classes = [AllowAny]

    def get(self, request, users_no=10):
        # it will fetch the data from the api and create users in the backend as much you want
        for _ in range(users_no):
            response_data = requests.get("https://randomuser.me/api/").json()
            user_info = response_data.get("results")[0]
            first_name = user_info.get("name").get("first")
            last_name = user_info.get("name").get("last")
            birth_date = user_info.get("dob").get("date").split("T")[0]
            age = user_info.get("dob").get("age")
            sex = user_info.get("gender")

            Person.objects.create(
                first_name=first_name, last_name=last_name, age=age, birth_date=birth_date, sex=sex)

        return Response(status_dict.get('success'))


class ApiCall(APIView):
    # Anyone is allowed to hit this url
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def __init__(self):
        self.male_user_firstnames = []
        self.male_user_lastnames = []
        self.male_dob_list = []
        self.final_male_list = []
        self.female_user_firstnames = []
        self.female_user_lastnames = []
        self.female_dob_list = []
        self.final_female_list = []
        self.count_male = 0
        self.count_female = 0
        self.final_list = []

    def get(self, request, user_no=5):
        print(user_no)
        try:
            qs = self.get_queryset()

            # sorting out the male users
            male_users = qs.filter(sex="male")

            # sorting out the female users
            female_users = qs.filter(sex="female")

            # destructuring the data of the list of male and female users to shuffle them further

            # destructured male users list
            for male_user in male_users:
                self.count_male += 1
                self.male_user_firstnames.append(male_user.first_name)
                self.male_user_lastnames.append(male_user.last_name)
                self.male_dob_list.append(
                    [{"birth_date": male_user.birth_date, "age": male_user.age}])

            # de-structured female users list
            for female_user in female_users:
                self.count_female += 1
                self.female_user_firstnames.append(female_user.first_name)
                self.female_user_lastnames.append(female_user.last_name)
                self.female_dob_list.append(
                    [{"birth_date": female_user.birth_date, "age": female_user.age}])

            # shuffling the lists to get random user data
            random.shuffle(self.male_user_firstnames)
            random.shuffle(self.male_user_lastnames)
            random.shuffle(self.male_dob_list)
            random.shuffle(self.female_user_firstnames)
            random.shuffle(self.female_user_lastnames)
            random.shuffle(self.female_dob_list)

            # coupling the shuffled data to form a user
            for i in range(self.count_male):
                male_user = {}
                male_user["first_name"] = self.male_user_firstnames[i]
                male_user["last_name"] = self.male_user_lastnames[i]
                male_user["dob"] = self.male_dob_list[i]
                male_user["sex"] = "male"
                self.final_male_list.append(male_user)
            for i in range(self.count_female):
                female_user = {}
                female_user["first_name"] = self.female_user_firstnames[i]
                female_user["last_name"] = self.female_user_lastnames[i]
                female_user["dob"] = self.female_dob_list[i]
                female_user["sex"] = "female"
                self.final_female_list.append(female_user)

            # final list prepared here
            self.final_male_list.extend(self.final_female_list)

            # shuffling the final user list
            random.shuffle(self.final_male_list)
            self.final_list = self.final_male_list

            # sending valid number of users keeping db and argument in view
            user_no = max(5, min(len(self.final_list), user_no))
            return Response(self.final_list[:user_no])
        except Exception as e:
            return Response(status_dict.get('fail'))

    def get_queryset(self):
        return Person.objects.all()



