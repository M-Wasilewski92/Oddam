document.addEventListener("DOMContentLoaded", function () {
    /**
     * Donation Form - Form section
     */


    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            // this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});


// Hiding Institutions without common category.
// Form Page 1
const category = document.querySelectorAll('.category-input')
const categoryChoice = []
let categoryId = ''
const formButtonOne = document.querySelector('#btn-slide-1')
formButtonOne.addEventListener('click', function (e) {
    category.forEach(category => {
        if (category.children[0].checked) {
            categoryChoice.push(category.children[0].value)
            categoryId += category.children[0].getAttribute('name')
        }
    })
})
// Form Page 2

// Button 'wstecz' clears category choices
const formBackButtonTwo = document.querySelector('#back-btn-2')
formBackButtonTwo.addEventListener('click', function (e) {
    categoryChoice.length = 0
})
// Removing institutions choices which no matching categories.

const institutionOptions = document.querySelectorAll('.institution-choice')
const formButtonTwo = document.querySelector('#btn-slide-2')
const noInstitutions = document.querySelector('.empty-list')

formButtonTwo.addEventListener('click', function (e) {

    let counter = 0
    institutionOptions.forEach(institution => {
        let categoryText = institution.children[2].children[2].innerText.split(" ")
        let hasCategory = categoryText.filter(category => categoryChoice.includes(category))
        if (!hasCategory.length > 0) {
            institution.style.display = 'none'
            counter++
        }
    })
    if (counter === institutionOptions.length) {
        noInstitutions.style.display = 'flex'
    }

})
// Form Step 3
const formButtonThree = document.querySelector('#btn-slide-3')
const institutionSummary = document.querySelector('.institution-summary')
const bagsSummary = document.querySelector('.bags-summary')
const bagsNumber = document.getElementById('bags')
let institutionId = 0
formButtonThree.addEventListener('click', function (e) {
    institutionOptions.forEach(institution => {
        if (institution.children[0].checked) {
            // Institution
            institutionId = institution.children[0].value
            let institutionName = institution.children[2].children[0].innerText


            const newSpanInstitution = document.createElement('span')
            newSpanInstitution.setAttribute('class', "summary--text")
            newSpanInstitution.innerText = `Dla Fundacji: ${institutionName}`
            institutionSummary.appendChild(newSpanInstitution)
            // Bags
            const newSpanBags = document.createElement('span')
            newSpanBags.setAttribute('class', "summary--text")
            newSpanBags.innerText = bagsNumber.value
            bagsSummary.appendChild(newSpanBags)
        }

    })


})

// function getInstitutionId () {
//         institutionOptions.forEach( institution => {
//             if (institution.children[0].checked) {
//                 // Institution
//                 let inst_id = institution.children[0].value
//                 return inst_id
//
//             }
//         })
//     }

const formBackButtonThree = document.querySelector('#back-btn-3')
formBackButtonThree.addEventListener('click', function (e) {
    institutionOptions.forEach(institution => {
            institution.style.display = 'flex'
        }
    )
})


// Form step 4
const formButtonFour = document.querySelector('#btn-slide-4')
// Get data from inputs and show them in summary

// Get institution to summary
const institutionChoiceField = document.querySelector('#institution-choice')
const addressDiv = document.querySelector('.address-list')
const pickUpDetails = document.querySelector('.pick-up-date')
// Get data to summary UserDetails
const address = document.querySelector('#address')
const city = document.querySelector('#city')
const postCode = document.querySelector('#postcode')
const phone = document.querySelector('#phone')
const pickUpDate = document.querySelector('#data')
const pickUpTime = document.querySelector('#time')
const moreInfo = document.querySelector('#more_info')
// Form Fields
const formQuantity = document.querySelector('#id_quantity')
const formAddress = document.querySelector('#id_address')
const formPhoneNumber = document.querySelector('#id_phone_number')
const formCity = document.querySelector('#id_city')
const formPostCode = document.querySelector('#id_zip_code')
const formPickUpDate = document.querySelector('#id_pick_up_date')
const formPickUpTime = document.querySelector('#id_pick_up_time')
const formPickUpComment = document.querySelector('#id_pick_up_comment')
const formInstitutionId = document.querySelector('#id_institution_id')
const formCategorysId = document.querySelector('#id_category_ids')

formButtonFour.addEventListener('click', function (e) {
    // Add user adres details
    let newAddressLi = document.createElement('li')
    newAddressLi.innerText = `Adres: ${address.value}`
    addressDiv.appendChild(newAddressLi)
    let newCityLi = document.createElement('li')
    newCityLi.innerText = `Miasto: ${city.value}`
    addressDiv.appendChild(newCityLi)
    let newPostCodeLi = document.createElement('li')
    newPostCodeLi.innerText = `Kod pocztowy: ul.${postCode.value}`
    addressDiv.appendChild(newPostCodeLi)
    let newPhoneLi = document.createElement('li')
    newPhoneLi.innerText = `Nr telefonu: ${phone.value}`
    addressDiv.appendChild(newPhoneLi)
    // Add pick up details
    let newPickUpDateLi = document.createElement('li')
    newPickUpDateLi.innerText = `Data odbioru: ${pickUpDate.value}`
    pickUpDetails.appendChild(newPickUpDateLi)
    let newPickUpTimeLi = document.createElement('li')
    newPickUpTimeLi.innerText = `Godzina odbioru: ${pickUpTime.value}`
    pickUpDetails.appendChild(newPickUpTimeLi)
    let newNoteLi = document.createElement('li')
    newNoteLi.innerText = `Uwagi dla kuriera: ${moreInfo.value}`
    pickUpDetails.appendChild(newNoteLi)
    // Send data to Form
    formQuantity.value = bagsNumber.value
    formAddress.value = address.value
    formPhoneNumber.value = phone.value
    formCity.value = city.value
    formPostCode.value = postCode.value
    formPickUpDate.value = pickUpDate.value
    formPickUpTime.value = pickUpTime.value
    formPickUpComment.value = moreInfo.value
    formInstitutionId.value = institutionId
    formCategorysId.value = categoryId
})

const formBackButtonFive = document.querySelector('#back-btn-5')
formBackButtonFive.addEventListener('click', function (e) {
    addressDiv.textContent = ''
    pickUpDetails.textContent = ''

})









