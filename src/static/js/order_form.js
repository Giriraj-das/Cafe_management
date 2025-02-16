document.addEventListener('DOMContentLoaded', function() {

    // Функция для привязки обработчиков к кнопкам удаления для новых строк
    function bindRemoveButtons() {
        document.querySelectorAll('.remove-dish').forEach(function(button) {
            // Удаляем предыдущий обработчик, чтобы не навешивать несколько раз
            button.removeEventListener('click', removeNewRowHandler);
            button.addEventListener('click', removeNewRowHandler);
        });
    }

    // Обработчик для кнопки удаления строки (для новых строк без поля DELETE)
    function removeNewRowHandler() {
        var dishRow = this.closest('.dish-row');
        if (!dishRow) return;

        // Если в строке есть поле DELETE, считаем, что это сохранённая строка – тогда не обрабатываем здесь.
        var deleteInput = dishRow.querySelector('input[name$="-DELETE"]');
        if (deleteInput) {
            return;
        } else {
            // Новая строка: проверяем количество строк
            var dishRows = document.querySelectorAll('#dish-formset .dish-row');
            if (dishRows.length > 1) {
                dishRow.parentNode.removeChild(dishRow);
                var totalFormsInput = document.querySelector('input[name="form-TOTAL_FORMS"]');
                if (totalFormsInput) {
                    totalFormsInput.value = parseInt(totalFormsInput.value) - 1;
                }
            } else {
                // Если это последняя строка, очищаем все её поля (при этом для поля количества ставим '1')
                dishRow.querySelectorAll('input').forEach(function(input) {
                    if (input.getAttribute('name').includes('quantity')) {
                        input.value = '1';
                    } else {
                        input.value = '';
                    }
                });
            }
        }
    }

    // Привязываем обработчики для кнопок удаления уже существующих новых строк
    bindRemoveButtons();

    // Обработчик для кнопки добавления новой строки
    var addDishBtn = document.getElementById('add-dish');
    if (addDishBtn) {
        addDishBtn.addEventListener('click', function() {
            var dishFormset = document.getElementById('dish-formset');
            var totalFormsInput = document.querySelector('input[name="form-TOTAL_FORMS"]');
            var currentFormCount = parseInt(totalFormsInput.value);

            // Клонируем первую строку как шаблон
            var template = dishFormset.firstElementChild;
            var newForm = template.cloneNode(true);

            // Удаляем из клона только элементы, связанные с удалением (поле DELETE и метку)
            var deleteInput = newForm.querySelector('input[name$="-DELETE"]');
            if (deleteInput && deleteInput.parentNode) {
                deleteInput.parentNode.removeChild(deleteInput);
            }
            var deleteLabel = newForm.querySelector('label[for="' + (deleteInput ? deleteInput.id : '') + '"]');
            if (deleteLabel && deleteLabel.parentNode) {
                deleteLabel.parentNode.removeChild(deleteLabel);
            }

            // Обновляем атрибуты name/id и очищаем значения в новой строке
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

            // Если в клоне уже есть кнопка удаления (с классом .remove-dish), оставляем её.
            // Если нет – добавляем её.
            if (!newForm.querySelector('.remove-dish')) {
                var removeBtn = document.createElement('button');
                removeBtn.type = 'button';
                removeBtn.className = 'remove-dish';
                removeBtn.textContent = '–';
                newForm.appendChild(removeBtn);
            }

            dishFormset.appendChild(newForm);
            totalFormsInput.value = currentFormCount + 1;

            // Привязываем обработчики к кнопкам удаления, включая новую строку
            bindRemoveButtons();
        });
    }
});
