def Diff(li1, li2):
    return list(list(set(li1) - set(li2)) + list(set(li2) - set(li1)))


def calcFiberunitSize(we, db):
    res = [we + 2 if we >= db.reserve_tv_zentral_fiber else 0]
    we += res[0]
    x = ['4er', '8er', '12er', '24er', '48er']
    y = [db.fiberunit_04, db.fiberunit_08, db.fiberunit_12, db.fiberunit_24, db.fiberunit_48]
    dict_fu = {x[i]: y[i] for i in range(len(x))}
    for key, value in dict_fu.items():
        if we <= value != 0:
            z = key
            break
    return z
