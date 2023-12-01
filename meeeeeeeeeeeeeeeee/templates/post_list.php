{% extends 'layout.html' %}

        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
{% block body %}

        <div class="mt-20 mb-20"></div>
        <table class="table table-striped table-hover">
            <thead>
                <tr>
                <th scope="col-1">No.</th>
                <th scope="col-2">Risk</th>
                <th scope="col-2">ID</th>
                <th scope="col-6">Content of the Post</th>
                <th scope="col-1">Delete</th>
                </tr>
            </thead>
            <tbody>
                
                   {% for new in newlist %}
                        <div class="row">
                    <tr>
                        <td>
                            <div class="col-1">{{new+1}}</div>
                        </td>
                        <td>
                            <div class="col-2">
                                {% if newlist[new][2] == 1%}
                                <img src="https://cdn.pixabay.com/photo/2012/04/12/20/12/x-30465_960_720.png" class="img-fluid" alt="Suspicious Content" width="400" height="400">
                                {% elif newlist[new][2] == 0%}
                                <img src="https://cdn-icons-png.flaticon.com/128/3643/3643948.png" class="img-fluid" alt="Safe Content" width="400" height="400">
                                {% endif %}
                            </div>
                        </td>
                        <td>
                            <div class="col-2">
                                {{newlist[new][1]}}
                            </div>
                        </td>
                        <td>
                            <div class="col-6">
                                {{newlist[new][0]}}
                            </div>
                        </td>
                        <td>
                            <div class="col-1">
                                <img src="https://cdn-icons-png.flaticon.com/128/216/216658.png" alt="Delete" width="50" height="50">
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                </div>
            </tbody>
        </table>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js" integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF" crossorigin="anonymous"></script>
{% endblock %}