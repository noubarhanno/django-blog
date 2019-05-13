$(document).ready(function () {
    var postForm = $(".form-like-ajax") // #form-product-ajax

    function likeThePost(postSlug, submitSpan) {
        var actionEndpoint = '/activities/like/'
        var httpMethod = 'GET'
        var data = {
            slug: postSlug
        }
        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: data,
            success: function (data) {
                console.log(data)
                console.log(data.owner)
                if (data.like) {
                    submitSpan.html("<button class='btn btn-primary'>Liked <i class='fas fa-thumbs-up'></i></button>")
                } else {
                    submitSpan.html("<button class='btn btn-secondary'>Like <i class='far fa-thumbs-up'></i></button>")
                }
            },
            error: function (error) {
                console.log(error)

            }
        })
    }

    postForm.submit(function (event) {
        event.preventDefault();
        console.log('Form is not sending')
        var $this = $(this)
        var submitSpan = $this.find('.submit-span')
        var likeInput = $this.find("[name='slug']")
        var postSlug = likeInput.attr('value')
        likeThePost(postSlug, submitSpan)
    })
})