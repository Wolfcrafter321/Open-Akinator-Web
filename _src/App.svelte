<script>
    let count = 0
</script>

<button on:click={() => count++}>
    {count}
</button>
<button class="svelte-button" on:click={() => count++}>
    {count}
</button>

<style>
    button {
        width: 100px;
        height: 50px;
    }
</style>