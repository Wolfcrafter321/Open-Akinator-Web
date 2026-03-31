<script>
    // export let onStart // 親から関数が渡されなかった場合に、{}を代入しておく
    export let onEdit = () => {}
    export let onStart = () => {}
    export let data = null

    console.log(data)

    function selectFile(e) {
        const file = e.target.files[0]
        if (file){
            const reader = new FileReader()
            reader.onload = (e) => {
                const text = e.target.result
                onStart(
                    {"data": text, "count": data["count"]+1}
                )
            }
            reader.readAsText(file)
        }
        else alert("ファイルが選択されませんでした")
    }

    function onStartDemo(e) {
        const file = {"name": "DEMO", "type": "application/json"}
        onStart(
            {"data": file, "count": data["count"]+1}
        )
    }
</script>

<h2>FileSelect</h2>
<input type="file" on:change={selectFile} />
<button on:click={onStartDemo}>Load DEMO</button>
<button on:click={onEdit}>Edit Mode</button>
