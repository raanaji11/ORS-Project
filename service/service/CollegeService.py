from service.models import College
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Role business logics.   
'''


class CollegeService(BaseService):

    def search(self, params):
        pageNo = (params["pageNo"] - 1) * self.pageSize
        sql = "select * from sos_college where 1=1"
        val = params.get("collegeName", None)
        if DataValidator.isNotNull(val):
            sql += " and collegeName = '" + val + " ' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ("id", "collegeName", "collegeAddress", "collegeState", "collegeCity", "collegePhoneNumber")
        res = {
            "data": []
        }
        count = 0
        for x in result:
            res["data"].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return College






'''dynamically generates query at runtime'''


'''Cursor class is an instance
 using which you can invoke methods
  that execute SQLite statements,
 fetch data from the result sets of the queries'''

'''MySQL provides a LIMIT clause that is used to specify the number of records to return.'''