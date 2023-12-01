import facebook
token='EAAJBlNIzKkQBACQC8Y0EFKDl7CQ2tfOgMkr8yNFK36ZAlGfkebUOKjqwOF0CP1ZBWwZCxgpAZAXSF945IwTIGn1rmcZAux5Q5hb2wMQqmO8nizGaLeLIsBlO3XT76QmwBtzn43iU6wiP0vdtZB7zTd4YCtlCntdhgkLvj1cUvsZCf5FvlkDkrph6GDWZAnCqI2UZD'
def get_text_of_post():
	try:
		graph=facebook.GraphAPI(access_token=token,version=3.1)
		posts=graph.request('101432762410121/posts')['data']
		newlist=[]
		for dic in posts:
			newlist.append(dic['message']) 
		print(type(newlist[0]))
	except Exception as e:
		print(e)

if __name__=='__main__':
    get_text_of_post()

