document.getElementById('add-dish').addEventListener('click', function() {
        var dishFormset = document.getElementById('dish-formset');
        var totalFormsInput = document.querySelector('input[name="form-TOTAL_FORMS"]');
        var currentFormCount = parseInt(totalFormsInput.value);

        var template = dishFormset.firstElementChild;
        var newForm = template.cloneNode(true);

        var inputs = newForm.querySelectorAll('input');
        inputs.forEach(function(input) {
            var nameAttr = input.getAttribute('name');
            if (nameAttr) {
                var newName = nameAttr.replace(/form-\d+-/, 'form-' + currentFormCount + '-');
                input.setAttribute('name', newName);
                input.setAttribute('id', 'id_' + newName);

                if (nameAttr.includes('quantity')) {
                    input.value = '1';
                } else {
                    input.value = '';
                }
            }
        });

        dishFormset.appendChild(newForm);
        totalFormsInput.value = currentFormCount + 1;
    });