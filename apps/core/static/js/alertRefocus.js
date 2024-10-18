if (focusTo) {
    const alertElements = document.getElementsByClassName('alert')
    if (alertElements) {
        Array.from(alertElements).forEach(
            async (e) => {
                e.addEventListener('closed.bs.alert', async function () {
                    document.getElementById(focusTo).focus()
                })
            }
        )
    }
}