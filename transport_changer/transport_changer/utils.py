def getargs(request, *keys, default_val=None):
    """
    Returns values as tuple from request args if exist else from request.form else from request.json
    :param request:             flask's Request object
    :param keys:                values to search by
    :param default_val:         default value if none was found
    :return:                    tuple of values
    """

    json = request.get_json(force=True, silent=True)
    out = []
    for key in keys:
        out.append(
            request.args.get(key) or request.form.get(key) or (
                json.get(key, default_val) if isinstance(json, dict) else default_val)
        )
    return tuple(out)

