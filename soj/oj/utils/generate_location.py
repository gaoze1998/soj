def generate_location(user_name, problem_id, language):
    suffix = ""
    if language == "C/C++":
        suffix = ".cpp"
    elif language == "Java":
        suffix = ".java"
    elif language == "Python3":
        suffix = ".py"
    return "./code/%s/%s" % (user_name, problem_id) + suffix
