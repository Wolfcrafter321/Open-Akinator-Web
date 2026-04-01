<script>
    import { onMount } from "svelte";

    export let onBack = () => {}
    export let data = null

    console.log(data)

    function matchFactor(featureVal, answer){
        return 1.0 - Math.abs(featureVal - answer)
    }

    // function updateProbabilities(characters, prob, questionKey, answer){
    //     let newProb = {}

    //     for (const c of characters){
    //         const name = c.name
    //         const featureVal = c.features[questionKey]

    //         let k;
    //         if (featureVal === undefined){
    //             k = 1.0
    //         } else {
    //             k = matchFactor(featureVal, answer)
    //         }

    //         newProb[name] = prob[name] * k
    //     }

    //     // normalize
    //     const total = Object.values(newProb).reduce((a, b) => a + b, 0)
    //     for (const name in newProb){
    //         newProb[name] /= total
    //     }

    //     return newProb
    // }
    
    function updateProbabilities(characters, prob, questionKey, answer){
        let newProb = {}

        for (const c of characters){
            const name = c.name
            const featureVal = c.features[questionKey]

            const k = (featureVal === undefined) ?
                1.0 : 
                matchFactor(featureVal, answer)

            newProb[name] = (prob[name] ?? 0) * k
        }

        // normalize
        const total = Object.values(newProb).reduce((a, b) => a + b, 0)

        if (!Number.isFinite(total) || total <= 0){
            // 全滅したらリセット、またはそのまま返す
            const uniform = 1 / characters.length
            for (const name in newProb) {
                newProb[name] = uniform
            }
            return newProb
        }

        for (const name in newProb){
            newProb[name] /= total
        }

        return newProb
    }

    function chooseBestQuestion(characters, remainingKeys){
        let bestKey = null
        let bestDiff = Infinity

        for (const key of remainingKeys){
           
            let sum = 0
            for(const c of characters){
                sum += (c.features[key] ?? 0)
            }
            const p = sum / characters.length

            const diff = Math.abs(p - 0.5)

            if (diff  < bestDiff){
                bestDiff = diff
                bestKey = key
            }
        }

        return bestKey
    }

    function collectAllFeatureKeys(characters) {
        const set = new Set()
        for (const c of characters) {
            for (const k in c.features) {
                set.add(k)
            }
        }

        return [...set]
    }


    let prob = {}
    let remainingKeys = []
    let step = 1

    let currentQuestion = null 
    let result = null
    let app_status = "standby" // "standby" | "asking" | "finished" | "no_more_questions"

    // run akinator!
    function runAkinator(characters){
        prob = {}
        for(const c of characters){
            prob[c.name] = 1 / characters.length
        }

        remainingKeys = collectAllFeatureKeys(characters)

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

        currentQuestion = chooseBestQuestion(data["data"], remainingKeys)
        remainingKeys = remainingKeys.filter(k => k !== currentQuestion)

        console.log(prob)
    }

    function answer(ans){
        prob = updateProbabilities(
            data["data"],
            prob,
            currentQuestion,
            ans
        )
        step ++
        nextStep()
    }

    onMount(()=>{
        if(data) runAkinator(data["data"])
    })

</script>

<button on:click={onBack}>Back</button>
<h2>Now Akinate!</h2>

{#if app_status === "asking"}
<p>質問 : {currentQuestion}</p>
<button on:click={()=>{answer(1.0)}}>はい</button>
<button on:click={()=>{answer(0.0)}}>いいえ</button>
<button on:click={()=>{answer(0.2)}}>どうだろう、わからない</button>
{:else if app_status === "finished"}
<p>答えは、{result}ですね！</p>
<button on:click={()=>{}}>はい</button>
<button on:click={()=>{}}>いいえ</button>
<button on:click={()=>{runAkinator(data["data"])}}>もういちど</button>
{:else if app_status === "no_more_questions"}
<p>尽力つきました...。答えは、{result}ですね？</p>
<button on:click={()=>{}}>はい</button>
<button on:click={()=>{}}>いいえ</button>
<button on:click={()=>{runAkinator(data["data"])}}>もういちど</button>
{:else}
<p>おっと... 想定外の結果となりました。</p>
<button on:click={()=>{runAkinator(data["data"])}}>もういちど</button>
{/if}
