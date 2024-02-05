import wepcore.downstream_services as services

prompt = "Input Raptor request: b[uilding] | t[emplate] | g[en token] c[reate incident]: "
request = input(prompt)

if request[0] == 'b':
	services.raptor_building_info()
elif request[0] == 'g':
	services.raptor_get_token()
else:
	print("Unknown request:", request)
pass
