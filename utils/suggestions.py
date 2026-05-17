def get_suggestion(level):

    if level == "Low":

        return """
        ✅ Low Stress
        
        Suggestions:
        - Maintain routine
        - Continue healthy sleep
        - Exercise regularly
        """

    elif level == "Medium":

        return """
        ⚠ Medium Stress
        
        Suggestions:
        - Meditation
        - Take short breaks
        - Reduce workload
        """

    else:

        return """
        🚨 High Stress
        
        Suggestions:
        - Proper rest
        - Counseling recommended
        - Reduce academic pressure
        - Talk to friends/family
        """