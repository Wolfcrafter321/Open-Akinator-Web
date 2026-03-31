<script>
    export let onBack = () => {}
    export let data = null

    console.log(data)

    let finished = false

    function matchFactor(featureVal, answer){
        return 1.0 - Math.abs(featureVal - answer)
    }

    function updateProbabilities(characters, prob, questionKey, answer){
        let newProb = {}

        for (const c of characters){
            const name = c.name
            const featureVal = c.features[questionKey]

            let k;
            if (featureVal === undefined){
                k = 1.0
            } else {
                k = matchFactor(featureVal, answer)
            }

            newProb[name] = prob[name] * k
        }

        // normalize
        const total = Object.values(newProb).reduce((a, b) => a + b, 0)
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

        const set = new Set();

        for (const c of characters) {
            for (const k in c.features) {
                set.add(k);
            }
        }

        return [...set];
    }


    // run akinator!


</script>

<button on:click={onBack}>Back</button>
<h2>Now Akinate!</h2>

{#if !finished}
<p>{finished}</p>
<button on:click={()=>{}}>はい</button>
<button on:click={()=>{}}>いいえ</button>
<button on:click={()=>{}}>どうだろう、わからない</button>
{:else}
<p>答えは、にわとりですね！</p>
<button on:click={()=>{}}>はい</button>
<button on:click={()=>{}}>いいえ</button>
{/if}
