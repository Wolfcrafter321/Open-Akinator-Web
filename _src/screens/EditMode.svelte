<script>
    import { slide } from "svelte/transition";

    export let onBack = () => {}
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
                data = {"data": parsedData, "count": data["count"]+1}
                onStart()
            }
            reader.readAsText(file)
        }
        else alert("ファイルが選択されませんでした")
    }

    async function onStartDemo(e) {
        try {
            const res = await fetch("/_src/data/data demo.json")
            const json = await res.json()
            data = {
                ...data,
                data: json,
                count: data["count"] + 1
            }
            onStart()
        }
        catch (err) {
            alert("DEMOデータの読み込みに失敗しました")
            console.error(err)
            return
        }
    }

    function onStart(){

    }

</script>

<button on:click={onBack}>Back</button>
<h2>Edit Mode</h2>
{#if !data["data"]}
<h3>File selection</h3>
<p>select a file!</p>
<input type="file" on:change={selectFile} />
<button on:click={onStartDemo}>Load DEMO</button>
{:else}
<h3>Lets Edit.</h3>
<p>let's edit!</p>
<p><input type="range" min="0" max="100" value="50" /></p>
<p><input type="range" min="0" max="100" value="50" /></p>
<p><input type="range" min="0" max="100" value="50" /></p>
<p><input type="range" min="0" max="100" value="50" /></p>
<button on:click={() => {data["data"] = null} }>Close File</button>
{/if}