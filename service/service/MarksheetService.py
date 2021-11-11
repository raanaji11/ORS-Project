from service.models import Marksheet
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection
'''
It contains Role business logics.   
'''


class MarksheetService(BaseService):

    def search(self, params):

        pageNo = (params["pageNo"] - 1) * self.pageSize
        sql = "select * from sos_marksheet where 1=1"
        val = params.get("rollNumber", None)
        if DataValidator.isNotNull(val):
            sql += " and rollNumber = '" + val + " ' "
        sql += " limit %s,%s"
        cursor = connection.cursor()

        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ("id", "rollNumber", "name", "physics", "chemistry", "maths")
        res = {
            "data": []
        }
        count = 0
        for x in result:

            res["data"].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Marksheet
