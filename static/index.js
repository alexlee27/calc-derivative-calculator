// All jQuery code goes below
// $ is shortcut for 'jQuery'
$(document).ready(function () {
    $("#differentiate").submit(function (event) {
        // Preventing submitting form by default
        event.preventDefault();

        const input = $("#input-text").val();
        const expand_bool = $("#expand").val();

        $.ajax({
            type: "POST",
            url: "/differentiate",
            data: { input_text: input, expand: expand_bool },
            dataType: "json",
            success: function (response) {
                // Update page with result
                var input_simplified = response.input_simplified;
                var differentiated_result = response.differentiated_result;

                input_simplified = "$$" + input_simplified + "$$";
                differentiated_result = "$$" + differentiated_result + "$$";

                const $input_simplified = $("#input-simplified");
                const $differentiated_result = $("#differentiated-result");

                $input_simplified.html(input_simplified)
                $differentiated_result.html(differentiated_result);

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
                var result = response.preview_result;
                result = "$$" + result + "$$";

                const $pTag = $("#input-preview");

                $pTag.html(result);

                MathJax.typesetPromise();
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });
});

function toggleExpandCheckbox() {
  var checkbox = document.getElementById("expand");
  checkbox.value = checkbox.checked;
}
