// All jQuery code goes below
// $ is shortcut for 'jQuery'
$(document).ready(function () {
    const loader = $("#loader");
    loader.hide();
    $("#differentiate").submit(function (event) {
        // Preventing submitting form by default
        event.preventDefault();

        const input = $("#input-text").val();
        const expandBool = $("#expand").val();
        const varOfDiff = $("#variable-of-diff").find(":selected").val();
        loader.show();
        console.log(varOfDiff);

        $.ajax({
            type: "POST",
            url: "/differentiate",
            data: { input_text: input, expand: expandBool, var_of_diff: varOfDiff },
            dataType: "json",
            success: function (response) {
                // Update page with result
                let input_simplified = response.input_simplified;
                let differentiated = response.differentiated;
                let input_simplified_string = response.input_simplified_string;
                let differentiated_string = response.differentiated_string;
                let expand = response.expand;
                let steps_latex = response.steps_latex;
                let steps_explanation = response.steps_explanation;
                let steps_explanation_latex = response.steps_explanation_latex;

                input_simplified = "$$" + input_simplified + "$$";
                differentiated = "$$" + differentiated + "$$";

                const $inputSimplified = $("#input-simplified");
                const $differentiatedResult = $("#differentiated-result");
                const $simplifyOriginal = $("#simplify-original");
                const $simplifyDifferentiated = $("#simplify-differentiated");
                const $simplifyExpand = $("#simplify-expand");
                const $steps = $("#steps");


                $inputSimplified.html(input_simplified);
                $differentiatedResult.html(differentiated);
                $simplifyOriginal.val(input_simplified_string);
                $simplifyDifferentiated.val(differentiated_string);
                $simplifyExpand.val(expand);

                $steps.empty();

                for (let i = 0; i < steps_latex.length; i++) {
                    explanation = "<div class=\"explanation\"><span>" + steps_explanation[i] + "</span>$$" + steps_explanation_latex[i] + "$$</div>";
                    step = "<div>$$" + steps_latex[i] + "$$</div>";
                    $steps.append(explanation);
                    $steps.append(step);
                }
                loader.hide();

                content.style.maxHeight = null;
                icon.textContent = "+";

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

    $("#input-text").on('input', inputPreview);

    $("#variable-of-diff").on('change', inputPreview);

    $("#simplify").submit(function (event) {
        // Preventing submitting form by default
        event.preventDefault();

        const simplifyOriginal = $("#simplify-original").val();
        const simplifyExpand = $("#simplify-expand").val();
        const varOfDiff = $("#variable-of-diff").find(":selected").val();
        loader.show();
        console.log(varOfDiff);

        $.ajax({
            type: "POST",
            url: "/differentiate",
            data: { input_text: simplifyOriginal, expand: simplifyExpand, var_of_diff: varOfDiff },
            dataType: "json",
            success: function (response) {
                // Update page with result
                let input_simplified = response.input_simplified;
                let differentiated = response.differentiated;
                let input_simplified_string = response.input_simplified_string;
                let differentiated_string = response.differentiated_string;
                let expand = response.expand;
                let steps_latex = response.steps_latex;
                let steps_explanation = response.steps_explanation;
                let steps_explanation_latex = response.steps_explanation_latex;

                input_simplified = "$$" + input_simplified + "$$";
                differentiated = "$$" + differentiated + "$$";

                const $inputSimplified = $("#input-simplified");
                const $differentiatedResult = $("#differentiated-result");
                const $simplifyOriginal = $("#simplify-original");
                const $simplifyDifferentiated = $("#simplify-differentiated");
                const $simplifyExpand = $("#simplify-expand");
                const $steps = $("#steps");


                $inputSimplified.html(input_simplified);
                $differentiatedResult.html(differentiated);
                $simplifyOriginal.val(input_simplified_string);
                $simplifyDifferentiated.val(differentiated_string);
                $simplifyExpand.val(expand);

                $steps.empty();

                for (let i = 0; i < steps_latex.length; i++) {
                    explanation = "<div class=\"explanation\"><span>" + steps_explanation[i] + "</span>$$" + steps_explanation_latex[i] + "$$</div>";
                    step = "<div>$$" + steps_latex[i] + "$$</div>";
                    $steps.append(explanation);
                    $steps.append(step);
                }
                loader.hide();

                content.style.maxHeight = null;
                icon.textContent = "+";

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

function inputPreview() {
    const input = $("#input-text").val();
    const $steps = $("#steps");
    const varOfDiff = $("#variable-of-diff").find(":selected").val();

    $steps.empty();
    icon.textContent = "+";

    $.ajax({
        type: "POST",
        url: "/input_preview",
        data: { input_text: input, var_of_diff: varOfDiff },
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
}

let coll = document.getElementById("show-steps");
let content = document.getElementById("steps");
let icon = document.getElementById("show-steps-icon");
coll.addEventListener("click", function() {
//    this.classList.toggle("active");
    if (content.style.maxHeight){
      content.style.maxHeight = null;
      content.style.paddingTop = 0;
      content.style.paddingBottom = 0;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }

    if (icon.textContent === "+") {
        icon.textContent = "−"; // U+2212; not a hyphen
    }
    else {
        icon.textContent = "+";
    }
});

let clearSteps = document.getElementById("clear-steps");
clearSteps.addEventListener("click", function() {
    while (content.firstChild) {
        content.removeChild(content.lastChild);
    }
    content.style.maxHeight = null;
    icon.textContent = "+";
});


function toggleExpandCheckbox() {
    let checkbox = document.getElementById("expand");
    checkbox.value = checkbox.checked;
}

function changeLaTeXStyle(idName, fontSize) {
    let div = document.getElementById(idName);
    let lst = div.getElementsByClassName("MathJax CtxtMenu_Attached_0")
    for (let i = 0; i < lst.length; i++){
        let latex = lst[i]
        latex.setAttribute("style", "font-size: " + fontSize.toString() + "%;");
    }
}

//function changeLaTeXStyleByClass(className, fontSize) {
//    let lst1 = document.getElementsByClassName(className);
//    for (let i = 0; i < lst1.length; i++) {
//        let latex = lst1[i].getElementsByClassName("MathJax CtxtMenu_Attached_0")[0]
//        latex.setAttribute("style", "font-size: " + fontSize.toString() + "%;");
//    }
//}

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
    if (latex.offsetWidth > div.offsetWidth - 200) {
        div.style.justifyContent = "flex-start";
        console.log('2');
        console.log(idName);
        console.log(latex.offsetWidth);
        console.log(div.offsetWidth - 200);
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
    if (latex.offsetWidth <= div.offsetWidth - 200) {
        div.style.justifyContent = "center";
        console.log('4');
        console.log(idName);
        console.log(latex.offsetWidth);
        console.log(div.offsetWidth - 200);
//        div.style.overflow = "auto";
    }

}
