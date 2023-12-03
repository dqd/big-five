let questions, personalInfo;

document.addEventListener('DOMContentLoaded', function() {
    const questionsElement = document.getElementById('questions');
    let questionSelector = ':scope > table.question';

    questions = questionsElement.querySelectorAll(questionSelector);
    questions.forEach(function(question) {
        question.style.display = 'none';
    });
    questionsElement.querySelectorAll(questionSelector + ' td > .control').forEach(function(control, i) {
        if (i > 0) {
            control.appendChild(createButton(translations.back, displayQuestion(i, -1))); // Vrátit se
        }

        if (i < questions.length - 1) {
            control.appendChild(createButton(translations.forward, displayQuestion(i, 1), true)); // Pokračovat dále
        }
    });

    personalInfo = document.getElementById('personal-info');

    const startButton = createButton(translations.start, startQuestionnaire, true); // Začít vyplňovat!

    personalInfo.querySelector('td > .control').appendChild(startButton);

    const selects = personalInfo.querySelectorAll('select');
    selects.forEach(function(select) {
        select.addEventListener('change', function() {
            startButton.disabled = Array.prototype.some.call(selects, function(x) {
                return x.value === '';
            });
        });
    });
});

function createButton(text, event, disabled) {
    const button = document.createElement('button');
    button.textContent = text;
    button.type = 'button';

    if (disabled) {
        button.disabled = disabled;
    }

    button.addEventListener('click', event);
    button.addEventListener('keyup', function(e) {
        if (['Enter', ' '].includes(e.key)) {
            event();
        }
    });

    return button;
}

function startQuestionnaire() {
    personalInfo.style.display = 'none';
    displayQuestion(-1, 1)();
}

function displayQuestion(index, increment) {
    return (function() {
        if (index >= 0) {
            questions[index].style.display = 'none';
        }

        const nextQuestion = questions[index + increment];
        nextQuestion.querySelectorAll('button:disabled').forEach(function(button) {
            nextQuestion.querySelectorAll('input[type="radio"]').forEach(function(radio) {
                function enableButton() {
                    button.disabled = false;
                    radio.removeEventListener('change', enableButton);
                }
                radio.addEventListener('change', enableButton);
            });
        });
        nextQuestion.style.display = '';
    });
}
