<script>
    export let onBack = () => {}
    export let data = null

    console.log(data)
</script>

<button on:click={onBack}>Back</button>
<h2>Now Akinate!</h2>

{#if true}
<p>それは赤いですか？</p>
<button on:click={()=>{}}>はい</button>
<button on:click={()=>{}}>いいえ</button>
<button on:click={()=>{}}>どうだろう、わからない</button>
{:else}
<p>答えは、にわとりですね！</p>
<button on:click={()=>{}}>はい</button>
<button on:click={()=>{}}>いいえ</button>
{/if}
