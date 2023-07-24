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
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });
})

function toggleExpandCheckbox() {
  var checkbox = document.getElementById("expand");
  checkbox.value = checkbox.checked;
}
