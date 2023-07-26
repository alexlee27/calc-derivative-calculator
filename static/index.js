let coll = document.getElementById("show-steps");
coll.addEventListener("click", function() {
    this.classList.toggle("active");
    let content = document.getElementById("steps");
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }

    let icon = document.getElementById("show-steps-icon");
    if (icon.textContent === "+") {
        icon.textContent = "−"; // U+2212; not a hyphen
    }
    else {
        icon.textContent = "+";
    }

});

// All jQuery code goes below
// $ is shortcut for 'jQuery'
$(document).ready(function () {
    $("#differentiate").submit(function (event) {
        // Preventing submitting form by default
        event.preventDefault();

        const input = $("#input-text").val();
        const expandBool = $("#expand").val();

        $.ajax({
            type: "POST",
            url: "/differentiate",
            data: { input_text: input, expand: expandBool },
            dataType: "json",
            success: function (response) {
                // Update page with result
                let input_simplified = response.input_simplified;
                let differentiated = response.differentiated;
                let input_simplified_string = response.input_simplified_string;
                let differentiated_string = response.differentiated_string;
                let expand = response.expand;

                input_simplified = "$$" + input_simplified + "$$";
                differentiated = "$$" + differentiated + "$$";

                const $inputSimplified = $("#input-simplified");
                const $differentiatedResult = $("#differentiated-result");
                const $simplifyOriginal = $("#simplify-original");
                const $simplifyDifferentiated = $("#simplify-differentiated");
                const $simplifyExpand = $("#simplify-expand");


                $inputSimplified.html(input_simplified);
                $differentiatedResult.html(differentiated);
                $simplifyOriginal.val(input_simplified_string);
                $simplifyDifferentiated.val(differentiated_string);
                $simplifyExpand.val(expand);

                MathJax.typesetPromise();
                OverflowChangeStyle("input-simplified");
                OverflowChangeStyle("differentiated-result");
                changeLaTeXStyle("input-simplified", 130);
                changeLaTeXStyle("differentiated-result", 130);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });

    $("#input-text").on('input', function() {
        const input = $("#input-text").val();

        $.ajax({
            type: "POST",
            url: "/input_preview",
            data: { input_text: input },
            dataType: "json",
            success: function (response) {
                // Update page with result
                let result = response.preview_result;
                result = "$$" + result + "$$";

                const $inputPreview = $("#input-preview");

                $inputPreview.html(result);

                MathJax.typesetPromise();
                changeLaTeXStyle("input-preview", 180);
                OverflowChangeStyle("input-preview");
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });

    $("#simplify").submit(function (event) {
        // Preventing submitting form by default
        event.preventDefault();

        const simplifyOriginal = $("#simplify-original").val();
        const simplifyExpand = $("#simplify-expand").val();

        $.ajax({
            type: "POST",
            url: "/differentiate",
            data: { input_text: simplifyOriginal, expand: simplifyExpand },
            dataType: "json",
            success: function (response) {
                // Update page with result
                let input_simplified = response.input_simplified;
                let differentiated = response.differentiated;
                let input_simplified_string = response.input_simplified_string;
                let differentiated_string = response.differentiated_string;
                let expand = response.expand;

                input_simplified = "$$" + input_simplified + "$$";
                differentiated = "$$" + differentiated + "$$";

                const $inputSimplified = $("#input-simplified");
                const $differentiatedResult = $("#differentiated-result");
                const $simplifyOriginal = $("#simplify-original");
                const $simplifyDifferentiated = $("#simplify-differentiated");
                const $simplifyExpand = $("#simplify-expand");


                $inputSimplified.html(input_simplified);
                $differentiatedResult.html(differentiated);
                $simplifyOriginal.val(input_simplified_string);
                $simplifyDifferentiated.val(differentiated_string);
                $simplifyExpand.val(expand);

                MathJax.typesetPromise();
                OverflowChangeStyle("input-simplified");
                OverflowChangeStyle("differentiated-result");
                changeLaTeXStyle("input-simplified", 130);
                changeLaTeXStyle("differentiated-result", 130);
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });
})

function toggleExpandCheckbox() {
    let checkbox = document.getElementById("expand");
    checkbox.value = checkbox.checked;
}

function changeLaTeXStyle(idName, fontSize) {
    let div = document.getElementById(idName);
    let latex = div.getElementsByClassName("MathJax CtxtMenu_Attached_0")[0]
    latex.setAttribute("style", "font-size: " + fontSize.toString() + "%;");
}

function OverflowChangeStyle(idName) {
    let div = document.getElementById(idName);
    let styles = getComputedStyle(div);
    let latex = div.getElementsByClassName("MathJax CtxtMenu_Attached_0")[0];
    if (latex.offsetHeight > div.offsetHeight - 50) {
        div.style.alignItems = "flex-start";
        console.log('1');
        console.log(idName);
        console.log(latex.offsetHeight);
        console.log(div.offsetHeight - 50);
//        div.style.overflow = "scroll";
    }
    if (latex.offsetWidth > div.offsetWidth - 135) {
        div.style.justifyContent = "flex-start";
        console.log('2');
        console.log(idName);
        console.log(latex.offsetWidth);
        console.log(div.offsetWidth - 135);
//        div.style.overflow = "scroll";
    }
    if (latex.offsetHeight <= div.offsetHeight - 50) {
        div.style.alignItems = "center";
        console.log('3');
        console.log(idName);
        console.log(latex.offsetHeight);
        console.log(div.offsetHeight - 50);
//        div.style.overflow = "auto";
    }
    if (latex.offsetWidth <= div.offsetWidth - 135) {
        div.style.justifyContent = "center";
        console.log('4');
        console.log(idName);
        console.log(latex.offsetWidth);
        console.log(div.offsetWidth - 135);
//        div.style.overflow = "auto";
    }

}
