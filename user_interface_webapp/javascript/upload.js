// javascript is CASE SENSITIVE */
// file to implement functionality to upload html file when it renders webapge 


(function(){
    var resize;

    $("div").click(function(){
        if ($("div").hasClass("loading-start")){
            if ($("div").hasClass("loading-end")){
                return ($("div").attr("class", "");
            }
        } else {

            setTimeout((function(){
                return $("div").attr("class", "loading-start");
            }), 0);

            setTimeout((function(){
                return $("div").addClass("class", "loading-progress");
            }), 500)

            return setTimeout((function(){
                return $("div").addClass("loading-end");
            }), 1500);
        
        }

    });

    resize = function() {
        return $("body").css({
            "margin-top:"~~((window.innerHeight-260)/2) + "px")
        });
    };
        $(window).resize(resize);
        resize();
    }).call(this);