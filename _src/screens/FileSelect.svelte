<script>
    // export let onStart // 親から関数が渡されなかった場合に、{}を代入しておく
    export let onEdit = () => {}
    export let onStart = () => {}

    function selectFile(e) {
        const file = e.target.files[0]
        if (file) onStart(file)
        else alert("ファイルが選択されませんでした")
    }
</script>

<h2>FileSelect</h2>
<input type="file" on:change={selectFile} />