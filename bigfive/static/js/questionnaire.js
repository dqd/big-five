'use strict';

// Turns the questionnaire into a wizard that shows one question at a time.
// Without JavaScript, the whole questionnaire is shown at once and still works.
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('questionnaire');
    const labels = JSON.parse(document.getElementById('questionnaire-labels').textContent);
    const personalInfo = document.getElementById('personal-info');
    const questions = Array.from(form.querySelectorAll('fieldset.question'));
    const progress = document.createElement('progress');
    // -1 stands for the personal info step.
    let current = -1;

    const createButton = (text, onClick, disabled = false) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = text;
        button.disabled = disabled;
        button.addEventListener('click', onClick);
        return button;
    };

    const isAnswered = (question) => question.querySelector('input[type="radio"]:checked') !== null;

    const stepElement = (index) => (index < 0 ? personalInfo : questions[index]);

    const show = (index) => {
        stepElement(current).hidden = true;
        stepElement(index).hidden = false;
        progress.hidden = index < 0;
        progress.value = Math.max(index, 0);
        current = index;
        form.scrollIntoView({ block: 'start' });
    };

    // Personal info step: the test can be started once both fields are filled in.
    const selects = Array.from(personalInfo.querySelectorAll('select'));
    const isPersonalInfoComplete = () => selects.every((select) => select.value !== '');
    const startButton = createButton(labels.start, () => show(0), !isPersonalInfoComplete());
    selects.forEach((select) => {
        select.addEventListener('change', () => {
            startButton.disabled = !isPersonalInfoComplete();
        });
    });
    personalInfo.querySelector('.control').append(startButton);

    // Questions: the next step is available once the question is answered.
    progress.max = questions.length;
    progress.hidden = true;
    document.getElementById('questions').prepend(progress);

    questions.forEach((question, index) => {
        const control = question.querySelector('.control');
        const isLast = index === questions.length - 1;
        const nextButton = isLast
            ? control.querySelector('button[type="submit"]')
            : createButton(labels.next, () => show(index + 1));

        nextButton.disabled = !isAnswered(question);
        question.querySelectorAll('input[type="radio"]').forEach((radio) => {
            radio.addEventListener('change', () => {
                nextButton.disabled = false;
            });
        });

        control.prepend(createButton(labels.back, () => show(index - 1)));
        if (!isLast) {
            control.append(nextButton);
        }
        question.hidden = true;
    });

    // Pressing Enter on a radio button would submit the whole form prematurely;
    // move to the next question instead.
    form.addEventListener('keydown', (event) => {
        if (event.key !== 'Enter' || current < 0 || current === questions.length - 1) {
            return;
        }

        event.preventDefault();
        const nextButton = questions[current].querySelector('.control > button:last-child');

        if (!nextButton.disabled) {
            nextButton.click();
        }
    });
});
