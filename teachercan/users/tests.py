from django.test import TestCase, Client

from config.api import api


class UserApiTest(TestCase):
    client = Client(api)

    def test_user_info_get(self):
        # 회원 가입
        self.client.post(
            "/api/auth/signup",
            {
                "email": "admin@admin.admin",
                "password": "1234512345!!",
                "nickname": "test_client",
            },
            content_type="application/json",
        )
        # 로그인
        response = self.client.post(
            "/api/auth/signin",
            {"email": "admin@admin.admin", "password": "1234512345!!"},
            content_type="application/json",
        )
        token = response.json()["data"]["token"]

        # 토큰 인증 성공
        response = self.client.get(
            "/api/user/info",
            HTTP_Authorization=f"Bearer {token}",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 200)
        data = response.json()["data"]
        self.assertEquals(data["email"], "admin@admin.admin")
        self.assertEquals(data["nickname"], "test_client")
        self.assertEquals(data["school"], None)

        # 토큰 없음
        response = self.client.get(
            "/api/user/info",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 401)

        # 토큰 인증 실패
        response = self.client.get(
            "/api/user/info",
            HTTP_Authorization=f"Bearer not_verified_token",
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 403)

    def test_user_info_put(self):
        # 회원가입
        self.client.post(
            "/api/auth/signup",
            {
                "email": "admin@admin.admin",
                "password": "1234512345!!",
                "nickname": "test_client",
            },
            content_type="application/json",
        )

        # 로그인
        response = self.client.post(
            "/api/auth/signin",
            {"email": "admin@admin.admin", "password": "1234512345!!"},
            content_type="application/json",
        )
        token = response.json()["data"]["token"]

        # social_id 수정
        response = self.client.put(
            "/api/user/info",
            {
                "socialId": "test_social_id",
            },
            content_type="application/json",
            HTTP_Authorization=f"Bearer {token}",
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["data"]["socialId"], "test_social_id")

        # nickname 수정
        response = self.client.put(
            "/api/user/info",
            {
                "nickname": "changed_nickname",
            },
            content_type="application/json",
            HTTP_Authorization=f"Bearer {token}",
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["data"]["nickname"], "changed_nickname")

        # gender 수정 에러(enum)
        response = self.client.put(
            "/api/user/info",
            {
                "gender": "사람",
            },
            content_type="application/json",
            HTTP_Authorization=f"Bearer {token}",
        )
        self.assertEquals(response.status_code, 422)

        # gender 수정 성공
        response = self.client.put(
            "/api/user/info",
            {
                "gender": "여",
            },
            content_type="application/json",
            HTTP_Authorization=f"Bearer {token}",
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["data"]["gender"], "여")

        # birthday 수정
        response = self.client.put(
            "/api/user/info",
            {
                "birthday": "1989-07-16",
            },
            content_type="application/json",
            HTTP_Authorization=f"Bearer {token}",
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["data"]["birthday"], "1989-07-16")

        # avatar_sgv 수정
        response = self.client.put(
            "/api/user/info",
            {
                "avatarSgv": "test_sgv.jpg",
            },
            content_type="application/json",
            HTTP_Authorization=f"Bearer {token}",
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["data"]["avatarSgv"], "test_sgv.jpg")

        # 학교 등록
        response = self.client.put(
            "/api/user/info",
            {
                "schoolCode": "7741021",
            },
            content_type="application/json",
            HTTP_Authorization=f"Bearer {token}",
        )
        self.assertEquals(response.status_code, 200)
        school = response.json()["data"]["school"]
        self.assertEquals(school["schoolCode"], "7741021")

        # 학교 수정
        response = self.client.put(
            "/api/user/info",
            {
                "schoolCode": "7751096",
            },
            content_type="application/json",
            HTTP_Authorization=f"Bearer {token}",
        )
        self.assertEquals(response.status_code, 200)
        school = response.json()["data"]["school"]
        self.assertEquals(school["schoolCode"], "7751096")
