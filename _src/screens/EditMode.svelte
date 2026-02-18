<script>
    export let onBack = () => {}

    function selectFile(e) {
        const file = e.target.files[0]
        if (file) onStart(file)
        else alert("ファイルが選択されませんでした")
    }
</script>

<button on:click={onBack}>Back</button>
<h2>Lets Edit.</h2>