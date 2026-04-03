<script>
    export let prob = {}
    let entries = []
    export let maxItems = 10

    console.log(prob)

    $: entries = Object.entries(prob)
        .sort((a,b)=> b[1]-a[1])
        .slice(0,maxItems)
</script>


<div class="panel">
    <h3>推論状況</h3>

    {#each entries as [name, p]}
    <div class="row">

        <div class="name">{name}</div>
        <div class="bar">
        <div class="fill" style="width:{p*100}%"></div>
        </div>

        <div class="value">
        {(p*100).toFixed(1)}%
        </div>

    </div>
    {/each}
</div>

<style>

.panel{
width:400px;
}

.panel::after{
content:"";
position:absolute;
left:0;
right:0;
bottom:0;
height:60px;

background:linear-gradient(
to bottom,
rgba(255,255,255,0),
rgba(255,255,255,1)
);
}

.row{
display:flex;
align-items:center;
gap:10px;
margin:6px 0;
}

.name{
width:80px;
font-weight:bold;
}

.bar{
flex:1;
height:12px;
background:#f3f3f3;
overflow:hidden;
}

.fill{
height:100%;
background:rgb(173, 173, 173);
}

.value{
width:60px;
font-size:12px;
}

</style>