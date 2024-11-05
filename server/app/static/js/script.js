const addBox = document.querySelector(".add-box"),
    popupBox = document.querySelector(".popup-box"),
    popupTitle = popupBox.querySelector("header p"),
    closeIcon = popupBox.querySelector("header i"),
    titleTag = popupBox.querySelector("input"),
    descTag = popupBox.querySelector("textarea"),
    addBtn = popupBox.querySelector("button");

const months = ["January", "February", "March", "April", "May", "June", "July",
                "August", "September", "October", "November", "December"];
let isUpdate = false, updateId;

addBox.addEventListener("click", () => {
    popupTitle.innerText = "Add a new Note";
    addBtn.innerText = "Add Note";
    popupBox.classList.add("show");
    document.querySelector("body").style.overflow = "hidden";
    if(window.innerWidth > 660) titleTag.focus();
});

closeIcon.addEventListener("click", () => {
    isUpdate = false;
    titleTag.value = descTag.value = "";
    popupBox.classList.remove("show");
    document.querySelector("body").style.overflow = "auto";
});

function showNotes() {
    fetch('/notes')
        .then(response => response.json())
        .then(notes => {
            const notesList = document.querySelector(".notes-list");
            notesList.innerHTML = ""; 
            notes.forEach(note => {
                let liTag = `<li class="note">
                                <div class="details">
                                    <p>${note.title}</p>
                                    <span>${note.content.replaceAll("\n", '<br/>')}</span>
                                </div>
                                <div class="bottom-content">
                                    <span>${note.created_at}</span>
                                    <div class="settings">
                                        <i onclick="showMenu(this)" class="uil uil-ellipsis-h"></i>
                                        <ul class="menu">
                                            <li onclick="updateNote(${note.id}, '${note.title}', '${note.content.replaceAll("'", "\\'")}')"><i class="uil uil-pen"></i>Edit</li>
                                            <li onclick="deleteNote(${note.id})"><i class="uil uil-trash"></i>Delete</li>
                                        </ul>
                                    </div>
                                </div>
                            </li>`;
                notesList.insertAdjacentHTML("beforeend", liTag);
            });
        });
}

function deleteAllNotes() {
    let confirmDel = confirm("Are you sure you want to delete all notes?");
    if (!confirmDel) return;

    fetch(`/delete_all_notes`, {
        method: "DELETE"
    })
    .then(response => {
        if (response.ok) {
            showNotes(); 
            location.reload();
        } else {
            alert("Error deleting all notes.");
        }
    });
}



function showMenu(elem) {
    elem.parentElement.classList.add("show");
    document.addEventListener("click", e => {
        if(e.target.tagName != "I" || e.target != elem) {
            elem.parentElement.classList.remove("show");
        }
    });
}

function deleteNote(noteId) {
    let confirmDel = confirm("Are you sure you want to delete this note?");
    if (!confirmDel) return;

    fetch(`/delete_note/${noteId}`, {
        method: "DELETE"
    })
    .then(response => {
        if (response.ok) {
            showNotes(); 
            location.reload();
        } else {
            alert("Error deleting note.");
        }
    });
}

function updateNote(noteId, title, content) {
    updateId = noteId;
    isUpdate = true;
    titleTag.value = title;
    descTag.value = content;
    popupTitle.innerText = "Update a Note";
    addBtn.innerText = "Update Note";
    popupBox.classList.add("show");
    document.querySelector("body").style.overflow = "hidden";
}

addBtn.addEventListener("click", e => {
    e.preventDefault();
    let title = titleTag.value.trim(),
        content = descTag.value.trim();

    if (title || content) {
        let noteData = { title, content };
        let url = isUpdate ? `/update_note/${updateId}` : '/notes';

        fetch(url, {
            method: isUpdate ? "POST" : "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(noteData),
        })
        .then(response => {
            if (response.ok) {
                showNotes(); 
                location.reload();
                closeIcon.click();
                isUpdate = false; 
                titleTag.value = descTag.value = ""; 
            } else {
                alert("Error saving note.");
            }
        })
        .catch(error => console.error('Error:', error));
    }
});

showNotes();

