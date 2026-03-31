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
                try {
                    JSON.parse(text)
                } catch (error) {
                    alert("ファイルを読み込めませんでした。")
                    console.log(error)
                    return
                }
                let parsedData = JSON.parse(text)
                onStart(
                    {"data": parsedData, "count": data["count"]+1}
                )
            }
            reader.readAsText(file)
        }
        else alert("ファイルが選択されませんでした")
    }

    async function onStartDemo(e) {
        try {
            const res = await fetch("/_src/data/data demo.json")
            const json = await res.json()

            onStart({
                data: json,
                count: data["count"] + 1
            })
        }
        catch (err) {
            alert("DEMOデータの読み込みに失敗しました")
            console.error(err)
            return
        }
    }
</script>

<h2>FileSelect</h2>
<input type="file" on:change={selectFile} />
<button on:click={onStartDemo}>Load DEMO</button>
<button on:click={onEdit}>Edit Mode</button>
