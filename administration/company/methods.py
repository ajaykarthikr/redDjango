from administration.models import (companyAdmin)


def addCompanyAdmin(u):
    return companyAdmin.objects.create(user=u)


def checkCompanyAdmin(u):
    return companyAdmin.objects.filter(user=u).exists()


def deleteCompanyAdmin(u):
    companyAdmin.objects.filter(user=u).delete()
