function bindCaptchaBtnClick() {
    $("#captcha-btn").on("click", function (event) {
        var $this = $(this)
        var email = $("input[name='email']").val()
        if (!email) {
            alert("Enter your email first！")
            return
        }
        $.ajax({
            url: "/user/captcha",
            method: "POST",
            data: {
                "email": email
            },
            success: function (res) {
                if (res['code'] === 200) {
                    $this.off("click");
                    var timeremain = 60;
                    var timer = setInterval(function () {
                        if (timeremain > 0) {
                            $this.text("Resend " + timeremain + "s later")
                            timeremain -= 1
                        } else {
                            $this.text("Verification Code")
                            bindCaptchaBtnClick()
                            clearInterval(timer)
                        }

                    }, 1000)
                    alert("Code sent!")
                } else {
                    alert(res['msg'])
                }
            }


        })

    })
}

// 网页文档加载完成
$(function () {
    bindCaptchaBtnClick();
})