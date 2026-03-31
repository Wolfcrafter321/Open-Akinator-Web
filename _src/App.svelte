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


{#if screen === "load"}
    <LoadScreen {data}      onStart={openQuestion} onEdit={openEdit} />
{:else if screen === "question"}
    <QuestionMode {data}    onBack={openLoad} />
{:else if screen === "edit"}
    <EditMode {data}        onBack={openLoad} />
{/if}
