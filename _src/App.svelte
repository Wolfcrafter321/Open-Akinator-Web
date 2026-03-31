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
// first load
import LoadScreen from './screens/FileSelect.svelte'
import QuestionMode from './screens/QuestionMode.svelte'
import EditMode from './screens/EditMode.svelte'

let data = {
    "data": null,
    "count": 0
}
let screen = "load"
// "load" | "question" | "edit"

function openLoad() {
    // data reset
    data={
    ...data,
    "data": null,
    // "count": 0 // inherit
    }
    screen = "load"
}
function openQuestion(_data) {
    data = {
    ...data,
    data: _data["data"],
    count: _data["count"]
    }
    screen = "question"
}
function openEdit() {
    screen = "edit"
}
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
    <LoadScreen {data}      onStart={openQuestion} onEdit={openEdit} />
{:else if screen === "question"}
    <QuestionMode {data}    onBack={openLoad} />
{:else if screen === "edit"}
    <EditMode {data}        onBack={openLoad} />
{/if}
