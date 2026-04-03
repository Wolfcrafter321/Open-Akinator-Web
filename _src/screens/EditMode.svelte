<script>
    import { slide } from "svelte/transition";

    export let onBack = () => {}
    export let data = null

    let file_loaded = false

    console.log(data)

    function selectFile(e) {
        const file = e.target.files[0]
        if (file) onStart(file)
        else alert("ファイルが選択されませんでした")
    }
</script>

<button on:click={onBack}>Back</button>
<h2>Edit Mode</h2>
{#if !file_loaded}
<h3>File selection</h3>
<p>select a file!</p>
<button on:click={() => {file_loaded=true} }>Load DEMO</button>
{:else}
<h3>Lets Edit.</h3>
<p>let's edit!</p>
<p><input type="range" min="0" max="100" value="50" /></p>
<p><input type="range" min="0" max="100" value="50" /></p>
<p><input type="range" min="0" max="100" value="50" /></p>
<p><input type="range" min="0" max="100" value="50" /></p>
<button on:click={() => {file_loaded=false} }>Clear DEMO</button>
{/if}