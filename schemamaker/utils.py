
def prep_for_kwargs(dictionary):
    if hasattr(dictionary, 'to_primitive'):
        return dictionary.to_primitive(dictionary)
    result = dict()
    for key, value in dictionary.iteritems():
        result[str(key)] = value
    return result
