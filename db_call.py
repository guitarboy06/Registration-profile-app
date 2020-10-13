from data_base import users


def db_call(username):
    prof = {}
    res = users.query.filter_by(user_name=username).first()
    name = res.name
    img_path = res.prof_img_path
    email = res.email
    phone = res.phone
    dob = res.dob
    guardian_name = res.guardian_name
    occupation = res.occupation
    address = res.address
    prof["name"] = name
    prof["img_path"] = img_path
    prof["email"] = email
    prof["phone"] = phone
    prof["dob"] = dob
    prof["guardian_name"] = guardian_name
    prof["occupation"] = occupation
    prof["address"] = address
    return prof
