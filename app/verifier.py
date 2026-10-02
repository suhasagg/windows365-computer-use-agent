from app.injection import scan
class UIVerifier:
    def verify(self,observations,trajectory):
        text=" ".join(str(x) for x in observations)
        inj=scan(text)
        failures=[x for x in trajectory if x.get("status")=="failed"]
        return {"verified":not failures and not inj["suspicious"],"prompt_injection":inj,"failures":failures,
                "observation_count":len(observations)}
verifier=UIVerifier()
