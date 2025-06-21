// tags-manager.js

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.tags-input').forEach(input => {
        new AccessibleTagManager(input);
    });
});

class AccessibleTagManager {
    constructor(input) {
        this.input = input;
        this.createUI();
        this.renderTags();
        this.setupEvents();
    }

    createUI() {
        this.container = document.createElement('div');
        this.container.className = 'tags-container';
        this.container.setAttribute('role', 'group');
        this.container.setAttribute('aria-labelledby', 'tags-label');

        this.input.classList.add('tags-original-input');
        this.input.hidden = true;

        const wrapper = document.createElement('div');
        wrapper.className = 'tags-wrapper';
        wrapper.innerHTML = `
            <div class="tags-visible-container" tabindex="0">
                <div class="tags-list" role="list"></div>
                <input type="text" class="tags-new-input"
                    role="textbox"
                    aria-label="Add a new tag"
                    aria-autocomplete="list"
                    aria-haspopup="listbox"
                    aria-multiline="false"
                >
            </div>
            <div class="tags-instructions">Press Enter to add tag. Use Backspace to remove.</div>
            <div class="sr-status" aria-live="polite" aria-atomic="true"></div>
        `;
        this.container.appendChild(wrapper);
        this.input.parentNode.insertBefore(this.container, this.input);

        this.tagsList = this.container.querySelector('.tags-list');
        this.newInput = this.container.querySelector('.tags-new-input');
        this.statusLive = this.container.querySelector('.sr-status');
    }

    renderTags() {
        this.tagsList.innerHTML = '';
        const tags = this.input.value.split(',').map(t => t.trim()).filter(Boolean);
        tags.forEach((tag, index) => {
            const tagEl = document.createElement('div');
            tagEl.className = 'tag';
            tagEl.setAttribute('role', 'listitem');
            tagEl.setAttribute('tabindex', '0');
            tagEl.innerHTML = `
                <span class="tag-text">${tag}</span>
                <button type="button" class="tag-remove"
                        role="button"
                        tabindex="0"
                        aria-label="❌ ${tag}"
                        data-index="${index}">
                    &times;
                </button>
            `;
            this.tagsList.appendChild(tagEl);
        });
    }

    setupEvents() {
        this.newInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && this.newInput.value.trim()) {
                this.addTag(this.newInput.value.trim());
                this.newInput.value = '';
                e.preventDefault();
            }
        });

        this.container.addEventListener('click', (e) => {
            if (e.target.classList.contains('tag-remove')) {
                const tagEl = e.target.closest('.tag');
                this.removeTag(tagEl);
            }
        });

        this.container.addEventListener('keydown', (e) => {
            if ((e.key === 'Backspace' || e.key === 'Delete') && document.activeElement.classList.contains('tag')) {
                this.removeTag(document.activeElement);
                e.preventDefault();
            }
            if ((e.key === 'Enter' || e.key === ' ') && e.target.classList.contains('tag-remove')) {
                this.removeTag(e.target.closest('.tag'));
                e.preventDefault();
            }
        });
    }

    addTag(tagText) {
        const currentTags = this.input.value.split(',').map(t => t.trim()).filter(Boolean);
        currentTags.push(tagText);
        this.input.value = currentTags.join(',');
        this.renderTags();
        this.statusLive.textContent = `Tag "${tagText}" added.`;
        this.newInput.focus();
    }

    removeTag(tagEl) {
        const index = [...this.tagsList.children].indexOf(tagEl);
        const currentTags = this.input.value.split(',').map(t => t.trim()).filter(Boolean);
        const removed = currentTags.splice(index, 1);
        this.input.value = currentTags.join(',');
        this.renderTags();
        this.statusLive.textContent = `Tag "${removed[0]}" removed.`;
        this.newInput.focus();
    }
}
