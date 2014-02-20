from django.shortcuts import render, render_to_response

def main(request):
    return render_to_response('map.html')
    
def about(request):
	return render_to_response('about.html')