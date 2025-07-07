let questions, personalInfo;

document.addEventListener('DOMContentLoaded', function() {
    const questionsElement = document.getElementById('questions');
    let questionSelector = ':scope > table.question',
        controlSelector = 'td > .control';

    questions = questionsElement.querySelectorAll(questionSelector);
    questions.forEach(function(question) {
        question.style.display = 'none';
    });
    questionsElement.querySelectorAll(questionSelector + ' ' + controlSelector).forEach(function(control, i) {
        if (i < questions.length - 1) {
            control.prepend(createButton(translations.forward, displayQuestion(i, 1), true));
        }

        if (i > 0) {
            control.prepend(createButton(translations.back, displayQuestion(i, -1)));
        }
    });

    personalInfo = document.getElementById('personal-info');

    const selects = personalInfo.querySelectorAll('select');
    const startButton = createButton(translations.start, startQuestionnaire, isStartButtonDisabled(selects));

    personalInfo.querySelector(controlSelector).appendChild(startButton);

    selects.forEach(function(select) {
        select.addEventListener('change', function() {
            startButton.disabled = isStartButtonDisabled(selects);
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

function isStartButtonDisabled(selects) {
    return Array.prototype.some.call(selects, function(x) {
        return x.value === '';
    });
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
