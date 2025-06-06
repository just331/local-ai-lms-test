lessons = {
"logic_programming": {
    display: "Logic Programming",
    questions: {
      "asp_ancestor_definition": {
        display: "Ancestor Relationship",
        description: "Write ASP rules to define when X is an ancestor of Y, including both base and recursive cases."
      },
      "answer_set_programming_definition": {
        display: "What is Answer Set Programming?",
        description: "Briefly describe what Answer Set Programming (ASP) is and its use cases."
      }
    }
  },
    "numbers_functions_expressions": {
    display: "Numbers, Functions, and Expressions",
    questions: {
      "function_comprehension": {
        display: "Function Comprehension",
        description: "Describe the purpose of the addition operator (+) as a function and then give an example using it and list its components: function, input, and value."
      },
      "set_comprehension": {
        display: "Expression Comprehension",
        description: "Can you explain how you determined the value of the expression 3 + 20, using the concepts of function, input and value?"
      }
    }
  },
    "fundamental_concepts_math_cs": {
    display: "Fundamental Concepts in Math and CS",
    questions: {
      "roster_notation": {
        display: "Roster Notation",
        description: "Write the set containing the numbers 4, 9, and 24 in roster notation."
      },
      "natural_numbers_def": {
        display: "Natural Numbers Definition",
        description: "Describe what a natural number is and why we don't consider 0 to apart of the natural set of numbers."
      }
    }
  },
};

const lessonSelect = document.getElementById("lesson_id");
const questionSelect = document.getElementById("question_id");
const questionDescription = document.getElementById("desc");
const submissionBox = document.getElementById("submission");

function renderLesson(){
    lessonSelect.innerHTML = "";
    for( const [lessonId, lesson] of Object.entries(lessons) ) {
        const option = document.createElement("option");
        option.value = lessonId;
        option.textContent = lesson.display;
        lessonSelect.appendChild(option);
    }
}

function renderQuestions() {
    const lessonId = lessonSelect.value;
    const questions = lessons[lessonId].questions;
    questionSelect.innerHTML = "";
    for( const [questionId, question] of Object.entries(questions) ) {
        const option = document.createElement("option");
        option.value = questionId;
        option.textContent = question.display;
        questionSelect.appendChild(option);
    }
}

function updateDescAndClear() {
  const lessonId = lessonSelect.value;
  const qId = questionSelect.value;
  questionDescription.textContent = lessons[lessonId].questions[qId].description;
  submissionBox.value = "";
  document.getElementById("result").textContent = "";
}

lessonSelect.onchange = function() {
    renderQuestions();
    updateDescAndClear();
};

questionSelect.onchange = updateDescAndClear;

window.onload = function() {
    renderLesson();
    renderQuestions();
    updateDescAndClear();
};

document.getElementById("llm-form").onsubmit = async function(e) {
      e.preventDefault();
      const lesson_id = document.getElementById("lesson_id").value;
      const question_id = questionSelect.value;
      const submission = document.getElementById("submission").value;
      document.getElementById("result").innerHTML = "Evaluating Submission...";
      try{

              const resp = await fetch("https://llm-lms-test.onrender.com/api/feedback/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              lesson_id,
              question_id,
              submission,
              // submission_type: "free_text" // Or "free_text" if appropriate
                //http://127.0.0.1:8000/api/feedback/
            })
          });
          const data = await resp.json();
          if(data.error){
              document.getElementById("result").innerHTML = `<span style="color: red;"><b>Error:</b> ${data.error}</span>`;
          }else{
              document.getElementById("result").innerHTML =
                    `<b>Feedback:</b><br><pre>${data.feedback}</pre>` +  `<b>Category:</b> ${data.category}`;
          }
      }catch (err) {
          document.getElementById("result").innerHTML = `<span style="color: red;"><b>Request failed:</b> ${err}</span>`;
      }

}