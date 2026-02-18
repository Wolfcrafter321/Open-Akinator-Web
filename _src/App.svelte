<!--

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
-->

<script>
  import LoadScreen from './screens/FileSelect.svelte'
  import QuestionMode from './screens/QuestionMode.svelte'
  import EditMode from './screens/EditMode.svelte'

  let screen = "load"
  // "load" | "question" | "edit"

  function openQuestion(ev) { screen = "question"; console.log(ev) }
  function openEdit() { screen = "edit" }
  function openLoad() { screen = "load" }
</script>


<!-- <button on:click={() => openLoad()}>
    <p>openLoad</p>
</button>
<button on:click={() => openQuestion()}>
    <p>openQuestion</p>
</button>
<button on:click={() => openEdit()}>
    <p>openEdit</p>
</button> -->


{#if screen === "load"}
  <LoadScreen onStart={openQuestion} onEdit={openEdit} />
{:else if screen === "question"}
  <QuestionMode onBack={openLoad} />
{:else if screen === "edit"}
  <EditMode onBack={openLoad} />
{/if}
