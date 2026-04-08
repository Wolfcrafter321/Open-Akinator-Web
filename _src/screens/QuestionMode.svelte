<script>
    import ProbabilityView from '/_src/screens/ProbabilityView.svelte'

    import { onMount } from "svelte";

    export let onBack = () => {}
    export let data = null

    console.log(data)

    
    let characters = null
    let questions = null
    
    let prob = {}
    let remainingKeys = []
    let step = 1
    let currentQuestion = null 
    let result = null
    let app_status = "standby" // "standby" | "asking" | "finished" | "no_more_questions"

    const UNKNOWN = 0.5

    function matchFactor(featureVal, answer){
        return 1.0 - Math.abs(featureVal - answer)
    }
    
    function entropy(p){

        if(p === 0 || p === 1) return 0
        return -p * Math.log2(p) - (1-p) * Math.log2(1-p)
    }

    function normalize(prob){
        // normalize
        const total = Object.values(prob).reduce((a, b) => a + b, 0)

        if (!Number.isFinite(total) || total <= 0){
            // 全滅したらリセット、またはそのまま返す
            const uniform = 1 / characters.length
            for (const name in prob) {
                prob[name] = uniform
            }
            return prob
        }

        for (const name in prob){
            prob[name] /= total
        }

        return prob
    }
    
    function updateProbabilities(prob, questionKey, answer){
        let newProb = {}

        for (const c of Object.keys(characters)){
            const name = c
            const featureVal = characters[c].features?.[questionKey] ?? UNKNOWN
            const k = matchFactor(featureVal, answer)
            newProb[name] = (prob[name] ?? 0) * k
        }

        // normalize
        newProb = normalize(newProb)

        return newProb
    }

    // function chooseBestQuestion(characters, remainingKeys){
    function chooseBestQuestion(remainingKeys, prob){
        let bestKey = null
        let bestScore = -Infinity

        for (const key of remainingKeys){
           
            let p = 0
            for(const c of Object.keys(characters)){
                const val = characters[c].features[key] ?? 0
                p += (prob[c] ?? 0) * val
            }

            const score = entropy(p)

            if(score > bestScore){
                bestScore = score
                bestKey = key
            }
        }


        return bestKey
    }

    function collectAllFeatureKeys() {
        const set = new Set()
        for (const c of Object.values(characters)) {
            for (const k in c.features) {
                set.add(k)
            }
        }

        return [...set]
    }



    // run akinator!
    function runAkinator(){
        prob = {}
        const chars = Object.keys(characters)
        for(const c of chars){
            prob[c] = 1 / chars.length
        }

        remainingKeys = collectAllFeatureKeys()

        step = 1
        app_status = "asking"
        result = null

        nextStep()
    }

    function nextStep(){
        let bestName = null
        let bestProb = -1

        for (const name in prob){
            if(prob[name] > bestProb){
                bestProb = prob[name]
                bestName = name
            }
        }

        if (bestProb >= 0.9){                   // thresholdを超えて終了
            app_status = "finished"
            result = bestName
            return
        }

        if (remainingKeys.length === 0){                   // 質問がなくて終了
            app_status = "no_more_questions"
            result = bestName
            return
        }

        currentQuestion = chooseBestQuestion(remainingKeys, prob)
        remainingKeys = remainingKeys.filter(k => k !== currentQuestion)

        console.log(prob)
    }

    function answer(ans){
        prob = updateProbabilities(
            prob,
            currentQuestion,
            ans
        )
        step ++
        nextStep()
    }

    onMount(()=>{
        if (!data) return
        
        characters = data["data"]["answers"]
        questions = data["data"]["questions"]

        runAkinator()
    })

</script>



<button on:click={onBack}>Back</button>
<div class="content">
    <div class="left">
        <h2>Now Akinate!</h2>

        {#if app_status === "asking"}
            <p class="message">質問 : {questions[currentQuestion]?.ja ?? currentQuestion}</p>
            <button on:click={()=>{answer(1.0)}}>はい</button>
            <button on:click={()=>{answer(0.0)}}>いいえ</button>
            <button on:click={()=>{answer(0.5)}}>どうだろう、わからない</button>
        {:else if app_status === "finished"}
            <p class="message">答えは、{result}ですね！</p>
            <button on:click={()=>{}}>はい</button>
            <button on:click={()=>{}}>いいえ</button>
            <button on:click={()=>{runAkinator(data["data"])}}>もういちど</button>
        {:else if app_status === "no_more_questions"}
            <p class="message">尽力つきました...。答えは、{result}ですか？</p>
            <button on:click={()=>{}}>はい</button>
            <button on:click={()=>{}}>いいえ</button>
            <button on:click={()=>{runAkinator(data["data"])}}>もういちど</button>
        {:else}
            <p class="message">おっと... 想定外の結果となりました。</p>
        {/if}

    </div>
    <div class="right">
        <!-- <ProbabilityView {prob} maxItems=5 /> -->
    </div>
</div>

<style>
.content{
display:flex;
gap:60px;
align-items:flex-start;
}

.left{
width:400px;
}

.right{
width:420px;
}

p.message{
    min-height: 50px;
    margin: 30px 0px 10px 30px;
}

</style>