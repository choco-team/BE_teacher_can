import json

from ninja.renderers import JSONRenderer


class DefaultRenderer(JSONRenderer):
    def render(self, request, data, *, response_status):
        # 성공
        if response_status < 400:
            res = {"success": True, "code": 2000}
            if type(data) == str:
                res.update({"message": data, "data": None})
            else:
                res.update({"message": None, "data": data})
        # 실패(예외처리)
        else:
            res = data

        return json.dumps(res, cls=self.encoder_class, **self.json_dumps_params)
