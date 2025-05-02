document.addEventListener('DOMContentLoaded', () => {
    const toggleGroups = {};
    console.log('toggleGroups', toggleGroups);

    document.querySelectorAll('.toggle').forEach((el, index) => {
        const groupName = el.dataset.togglename;
        console.log(groupName);
        if (!groupName) return;

        if (!toggleGroups[groupName]) toggleGroups[groupName] = [];

        toggleGroups[groupName].push(el);
    });

    Object.values(toggleGroups).forEach((group) => {
        // Hide all but the first
        group.forEach((el, i) => {
            el.style.display = i === 0 ? '' : 'none';
        });

        group.forEach((el) => {
            el.addEventListener('click', () => {
                const currentIndex = group.findIndex((e) => e.style.display !== 'none');
                const nextIndex = (currentIndex + 1) % group.length;

                group[currentIndex].style.display = 'none';
                group[nextIndex].style.display = '';
            });
        });
    });
});
