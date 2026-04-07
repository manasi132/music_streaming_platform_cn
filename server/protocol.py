def parse_request(request):
    try:
        request = request.strip()

        if request.startswith("GET"):
            parts = request.split()
            if len(parts) == 2:
                return parts[1]

        return None

    except Exception as e:
        print("[PROTOCOL ERROR]", e)
        return None